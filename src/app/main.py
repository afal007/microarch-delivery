import contextvars
import logging
import uuid
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.adapters.in_.http.apis.couriers_api import courier_router
from app.adapters.in_.http.apis.orders_api import order_router
from app.adapters.in_.jobs.jobs import DispatchOrdersJob, MoveCouriersJob
from app.ioc.composition_root import container


def create_scheduler(
        move_job: MoveCouriersJob,
        dispatch_job: DispatchOrdersJob,
) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        move_job.run,
        trigger=IntervalTrigger(seconds=1),
        name="Move Couriers Every 1s"
    )
    scheduler.add_job(
        dispatch_job.run,
        trigger=IntervalTrigger(seconds=2),
        name="Dispatch Orders Every 2s"
    )
    return scheduler


trace_id_var = contextvars.ContextVar("trace_id", default="-")
request_id_var = contextvars.ContextVar("request_id", default="-")
span_id_var = contextvars.ContextVar("span_id", default="-")
app_name_var = contextvars.ContextVar("app_name", default="-")
user_id_var = contextvars.ContextVar("user_id", default="-")
event_dataset_var = contextvars.ContextVar("event_dataset_var", default="default")


def set_trace_id(value: str): trace_id_var.set(value)


def set_request_id(value: str): request_id_var.set(value)


def set_span_id(value: str): span_id_var.set(value)


def set_app_name(value: str): app_name_var.set(value)


def set_user_id(value: str): user_id_var.set(value)


def get_trace_id(): return trace_id_var.get()


def get_request_id(): return request_id_var.get()


def get_span_id(): return span_id_var.get()


def get_app_name(): return app_name_var.get()


def get_user_id(): return user_id_var.get()


def get_event_dataset(): return event_dataset_var.get()


def generate_trace_id() -> str:
    return uuid.uuid4().hex[:32]  # 64-bit trace ID (hex)


def generate_span_id() -> str:
    return uuid.uuid4().hex[:16]


debug = logging.getLogger("debug")


class LogContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.user_id = get_user_id()
        record.trace_id = get_trace_id()
        record.span_id = get_span_id()
        record.event_dataset = get_event_dataset()
        record.service_name = 'microarch-delivery'
        return True


http_logger = logging.getLogger("http")


class B3LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        debug.info("Setting up contextvars")
        trace_id = request.headers.get("x-b3-traceid", generate_trace_id())
        span_id = request.headers.get("x-b3-spanid", generate_span_id())
        user_id = request.headers.get("x-user", '-')

        set_trace_id(trace_id)
        set_span_id(span_id)
        set_user_id(user_id)
        # set_request_id(request_id)

        response = await call_next(request)

        # Добавим trace ID в response для проксей или клиента
        response.headers["x-b3-traceid"] = trace_id
        response.headers["x-b3-spanid"] = span_id

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_body = await request.body()
        http_logger.info({
            "event.dataset": "http",
            "message": f"REQUEST",
            "http.request.method": request.method,
            "http.request.body.content": request_body.decode(errors="ignore"),
            "url.path": request.url.path,
            "url.full": str(request.url),
        })

        # Получаем оригинальный response
        response = await call_next(request)

        # Сохраняем тело ответа
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        http_logger.info({
            "event.dataset": "http",
            "message": f"RESPONSE",
            "http.response.status_code": response.status_code,
            "http.response.body.content": response_body.decode(errors="ignore"),
            "url.path": request.url.path,
            "url.full": str(request.url),
        })

        # Возвращаем новый response с тем же телом
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_context_filter = LogContextFilter()

    # Пройтись по всем логгерам, включая root
    for logger_name in logging.root.manager.loggerDict:
        logger = logging.getLogger(logger_name)

        # Убедиться, что у логгера есть handlers
        if hasattr(logger, "handlers"):
            for handler in logger.handlers:
                handler.addFilter(log_context_filter)

    # Не забудь root-логгер
    for handler in logging.getLogger().handlers:
        handler.addFilter(log_context_filter)

    move_job = await container.get(MoveCouriersJob)
    dispatch_job = await container.get(DispatchOrdersJob)

    scheduler = create_scheduler(move_job, dispatch_job)
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(order_router)
app.include_router(courier_router)
app.add_middleware(LoggingMiddleware)
app.add_middleware(B3LoggingMiddleware)

setup_dishka(container, app)

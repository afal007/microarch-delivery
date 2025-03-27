import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.adapters.in_.http.apis.couriers_api import courier_router
from app.adapters.in_.http.apis.orders_api import order_router
from app.adapters.in_.jobs.jobs import DispatchOrdersJob, MoveCouriersJob
from app.ioc.composition_root import container

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
)


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    move_job = await container.get(MoveCouriersJob)
    dispatch_job = await container.get(DispatchOrdersJob)

    scheduler = create_scheduler(move_job, dispatch_job)
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(order_router)
app.include_router(courier_router)
setup_dishka(container, app)

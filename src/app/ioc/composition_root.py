from dishka import make_async_container

from app.ioc.dispatch_service_provider import DispatchServiceProvider

container = make_async_container(DispatchServiceProvider())

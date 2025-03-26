from dishka import make_async_container

from app.ioc.config_provider import ConfigProvider
from app.ioc.dispatch_service_provider import DispatchServiceProvider
from app.ioc.repository_provider import RepositoryProvider
from app.ioc.sqlalchemy_provider import SqlAlchemyProvider

container = make_async_container(
    ConfigProvider()
    , SqlAlchemyProvider()
    , RepositoryProvider()
    , DispatchServiceProvider()
)

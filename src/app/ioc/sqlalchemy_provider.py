from dynaconf import Dynaconf
from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, create_async_engine


class SqlAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def get_async_manager(self, async_engine: AsyncEngine) -> async_sessionmaker:
        return async_sessionmaker(async_engine)

    @provide(scope=Scope.APP)
    def get_async_engine(self, settings: Dynaconf) -> AsyncEngine:
        return create_async_engine(
            settings.postgres.dsn,
            pool_size=settings.postgres.pool_size,
            pool_recycle=settings.postgres.pool_recycle,
            max_overflow=settings.postgres.max_overflow,
            echo=settings.postgres.echo,
        )

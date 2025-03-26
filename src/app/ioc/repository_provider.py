from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.adapters.out.postgresql.order.order_repository import OrderRepository
from app.core.ports.i_order_repository import IOrderRepository


class RepositoryProvider(Provider):
    @provide(scope=Scope.APP)
    def get_order_repository(self, session_factory: async_sessionmaker) -> IOrderRepository:
        return OrderRepository(session_factory)

from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select

from app.adapters.out.postgresql.order.order_db import OrderDB
from app.core.domain.model.order.order import Order, OrderStatus
from app.core.ports.order_repository import IOrderRepository


class OrderRepository(IOrderRepository):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    async def add(self, order: Order) -> None:
        async with self.session_factory() as session:
            session.add(OrderDB.from_domain(order))
            await session.commit()

    async def update(self, order: Order) -> None:
        async with self.session_factory() as session:
            order_db = await session.get(OrderDB, order.id)
            order_db.update_from_domain(order)
            await session.commit()

    async def get_by_id(self, order_id: UUID) -> Order | None:
        async with self.session_factory() as session:
            order_model = await session.get(OrderDB, order_id)
            return order_model.to_domain() if order_model else None

    async def get_all_new(self) -> List[Order]:
        async with self.session_factory() as session:
            result = await session.execute(select(OrderDB).filter_by(status=OrderStatus.CREATED.value))
            return [row.to_domain() for row in result.scalars()]

    async def get_all_assigned(self) -> List[Order]:
        async with self.session_factory() as session:
            result = await session.execute(select(OrderDB).filter_by(status=OrderStatus.ASSIGNED.value))
            return [row.to_domain() for row in result.scalars()]

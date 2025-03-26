import uuid
import random
from dataclasses import dataclass

from app.core.application.usecases.common.command import Command
from app.core.domain.kernel.location import Location
from app.core.domain.model.order.order import Order
from app.core.ports.i_order_repository import IOrderRepository


@dataclass
class CreateOrderCommand(Command):
    order_id: uuid.UUID
    street: str | None  # пока игнорируется, будет использоваться после интеграции с Geo


class CreateOrderHandler:
    def __init__(self, order_repository: IOrderRepository):
        self._order_repository = order_repository

    async def handle(self, command: CreateOrderCommand) -> None:
        location = Location(
            x=random.randint(1, 10),
            y=random.randint(1, 10)
        )
        order = Order.create_new(id=command.order_id, location=location)
        await self._order_repository.add(order)

import uuid
from abc import abstractmethod

from pydantic import BaseModel, Field, field_validator

from app.core.application.usecases.common.command import Command, ICommandHandler
from app.core.domain.model.order.order import Order
from app.core.ports.geo_client import IGeoClient
from app.core.ports.order_repository import IOrderRepository


class CreateOrderCommand(BaseModel, Command):
    order_id: uuid.UUID
    street: str = Field(..., min_length=1)

    @field_validator("street")
    @classmethod
    def strip_and_validate(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Street must not be empty or whitespace")
        return v


class ICreateOrderHandler(ICommandHandler):
    @abstractmethod
    async def handle(self, command: CreateOrderCommand) -> None:
        pass


class CreateOrderHandler(ICreateOrderHandler):
    def __init__(self, order_repository: IOrderRepository, geo_client: IGeoClient):
        self._geo_client = geo_client
        self._order_repository = order_repository

    async def handle(self, command: CreateOrderCommand) -> None:
        order = Order.create_new(id=command.order_id, location=await self._geo_client.get_geolocation(command.street))
        await self._order_repository.add(order)

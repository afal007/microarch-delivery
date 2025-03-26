from uuid import UUID
from typing import List
from pydantic import BaseModel

from app.core.application.usecases.common.location_dto import LocationDTO
from app.core.application.usecases.common.query import Query
from app.core.ports.i_order_repository import IOrderRepository
from app.core.domain.model.order.order import Order


class OrderDTO(BaseModel):
    id: UUID
    location: LocationDTO


class GetUnfinishedOrdersQuery(Query):
    pass


class GetUnfinishedOrdersHandler:
    def __init__(self, order_repository: IOrderRepository):
        self._order_repository = order_repository

    async def handle(self, query: GetUnfinishedOrdersQuery) -> List[OrderDTO]:
        # TODO: оптимизировать одним запросом
        created = await self._order_repository.get_all_new()
        assigned = await self._order_repository.get_all_assigned()
        orders: List[Order] = created + assigned

        return [
            OrderDTO(
                id=o.id,
                location=LocationDTO(o.location.x, o.location.y)
            ) for o in orders
        ]

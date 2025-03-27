from abc import abstractmethod
from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.core.application.usecases.common.location_dto import LocationDTO
from app.core.application.usecases.common.query import IQueryHandler, Query
from app.core.domain.model.courier.courier import Courier
from app.core.ports.i_courier_repository import ICourierRepository


class CourierDTO(BaseModel):
    id: UUID
    name: str
    location: LocationDTO


class GetAllCouriersQuery(Query):
    pass


class IGetAllCouriersHandler(IQueryHandler):
    @abstractmethod
    async def handle(self, query: GetAllCouriersQuery) -> List[CourierDTO]:
        pass


class GetAllCouriersHandler(IGetAllCouriersHandler):
    def __init__(self, courier_repository: ICourierRepository):
        self._courier_repository = courier_repository

    async def handle(self, query: GetAllCouriersQuery) -> List[CourierDTO]:
        couriers: List[Courier] = await self._courier_repository.get_all()
        return [
            CourierDTO(
                id=c.id,
                name=c.name,
                location=LocationDTO(c.location.x, c.location.y)
            ) for c in couriers
        ]

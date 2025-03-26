from uuid import UUID
from typing import List
from pydantic import BaseModel

from app.core.application.usecases.common.query import Query
from app.core.application.usecases.common.location_dto import LocationDTO
from app.core.ports.i_courier_repository import ICourierRepository
from app.core.domain.model.courier.courier import Courier


class CourierDTO(BaseModel):
    id: UUID
    name: str
    location: LocationDTO


class GetAllCouriersQuery(Query):
    pass


class GetAllCouriersHandler:
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

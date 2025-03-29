from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select

from app.adapters.out.postgresql.courier.courier_db import CourierDB
from app.adapters.out.postgresql.courier.transport_db import TransportDB
from app.core.domain.model.courier.courier import Courier, CourierStatus
from app.core.ports.courier_repository import ICourierRepository


class CourierRepository(ICourierRepository):
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory

    async def add(self, courier: Courier) -> None:
        async with self._session_factory() as session:
            transport_model = TransportDB.from_domain(courier.transport)
            courier_model = CourierDB.from_domain(courier)
            session.add_all([transport_model, courier_model])
            await session.commit()

    async def update(self, courier: Courier) -> None:
        async with self._session_factory() as session:
            courier_db = await session.get(CourierDB, courier.id)
            courier_db.update_from_domain(courier)
            await session.commit()

    async def get_by_id(self, courier_id: UUID) -> Courier | None:
        async with self._session_factory() as session:
            courier_db = await session.get(CourierDB, courier_id)
            return courier_db.to_domain() if courier_db else None

    async def get_all_free(self) -> List[Courier]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(CourierDB).filter_by(status=CourierStatus.FREE.value)
            )
            return [row.to_domain() for row in result.scalars().all()]

    async def get_all(self) -> List[Courier]:
        async with self._session_factory() as session:
            result = await session.execute(select(CourierDB))
            return [row.to_domain() for row in result.scalars().all()]

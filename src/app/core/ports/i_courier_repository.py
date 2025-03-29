from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.core.domain.model.courier.courier import Courier


class ICourierRepository(ABC):
    @abstractmethod
    async def add(self, courier: Courier) -> None:
        pass

    @abstractmethod
    async def update(self, courier: Courier) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, courier_id: UUID) -> Courier | None:
        pass

    @abstractmethod
    async def get_all_free(self) -> List[Courier]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Courier]:
        pass

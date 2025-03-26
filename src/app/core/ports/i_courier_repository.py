from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.core.domain.model.courier.courier import Courier


class ICourierRepository(ABC):
    @abstractmethod
    def add(self, courier: Courier) -> None:
        pass

    @abstractmethod
    def update(self, courier: Courier) -> None:
        pass

    @abstractmethod
    def get_by_id(self, courier_id: UUID) -> Courier | None:
        pass

    @abstractmethod
    def get_all_free(self) -> List[Courier]:
        pass

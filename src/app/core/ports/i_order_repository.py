from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.core.domain.model.order.order import Order


class IOrderRepository(ABC):
    @abstractmethod
    async def add(self, order: Order) -> None:
        pass

    @abstractmethod
    async def update(self, order: Order) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None:
        pass

    @abstractmethod
    async def get_all_new(self) -> List[Order]:
        pass

    @abstractmethod
    async def get_all_assigned(self) -> List[Order]:
        pass

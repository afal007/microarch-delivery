from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.core.domain.model.order.order import Order


class IOrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order) -> None:
        pass

    @abstractmethod
    def update(self, order: Order) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None:
        pass

    @abstractmethod
    def get_all_new(self) -> List[Order]:
        pass

    @abstractmethod
    def get_all_assigned(self) -> List[Order]:
        pass

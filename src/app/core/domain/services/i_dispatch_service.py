from abc import ABC, abstractmethod
from typing import List
from app.core.domain.model.order.order import Order
from app.core.domain.model.courier.courier import Courier


class IDispatchService(ABC):
    @abstractmethod
    async def dispatch(self, order: Order, couriers: List[Courier]) -> Courier | None:
        """Find the best courier and assign them to the order."""
        pass

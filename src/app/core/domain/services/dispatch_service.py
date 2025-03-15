from typing import List
from app.core.domain.model.order.order import Order, OrderStatus
from app.core.domain.model.courier.courier import Courier, CourierStatus
from app.core.domain.services.i_dispatch_service import IDispatchService


class DispatchService(IDispatchService):
    async def dispatch(self, order: Order, couriers: List[Courier]) -> Courier | None:
        """Assigns the best courier to the order based on delivery speed."""

        if order.status != OrderStatus.CREATED:
            raise ValueError("Order must be in CREATED status to be dispatched.")

        free_couriers = [courier for courier in couriers if courier.status == CourierStatus.FREE]

        if not free_couriers:
            return None  # No available couriers

        # Select the best courier based on shortest delivery time
        best_courier = min(free_couriers, key=lambda c: c.steps_to_order(order.location))

        # Assign the best courier to the order
        order.assign_courier(best_courier.id)
        best_courier.set_status_busy()

        return best_courier

import uuid
import pytest
from unittest.mock import AsyncMock
from app.core.application.usecases.commands.move_couriers import MoveCouriersCommand, MoveCouriersHandler
from app.core.domain.kernel.location import Location
from app.core.domain.model.order.order import Order, OrderStatus
from app.core.domain.model.courier.courier import Courier, CourierStatus
from app.core.domain.model.courier.courier import TransportParams


@pytest.mark.asyncio
async def test_move_couriers_courier_moves_closer():
    order = Order.create_new(id=uuid.uuid4(), location=Location(x=5, y=5))

    courier = Courier.create(
        name="John",
        transport_params=TransportParams(name="bike", speed=1),
        location=Location(x=1, y=1)
    )
    order.assign_courier(courier.id)
    courier.set_status_busy()

    mock_order_repo = AsyncMock()
    mock_order_repo.get_all_assigned.return_value = [order]
    mock_order_repo.update = AsyncMock()

    mock_courier_repo = AsyncMock()
    mock_courier_repo.get_by_id.return_value = courier
    mock_courier_repo.update = AsyncMock()

    handler = MoveCouriersHandler(
        order_repository=mock_order_repo,
        courier_repository=mock_courier_repo
    )

    await handler.handle(MoveCouriersCommand())

    assert mock_courier_repo.update.called
    assert mock_order_repo.update.called is False
    assert courier.location != order.location
    assert order.status == OrderStatus.ASSIGNED
    assert courier.status == CourierStatus.BUSY


@pytest.mark.asyncio
async def test_move_couriers_courier_reaches_order():
    location = Location(x=4, y=1)
    order = Order.create_new(id=uuid.uuid4(), location=location)

    courier = Courier.create(
        name="John",
        transport_params=TransportParams(name="bike", speed=3),  # Big step to reach immediately
        location=Location(x=1, y=1)
    )
    order.assign_courier(courier.id)
    courier.set_status_busy()

    mock_order_repo = AsyncMock()
    mock_order_repo.get_all_assigned.return_value = [order]
    mock_order_repo.update = AsyncMock()

    mock_courier_repo = AsyncMock()
    mock_courier_repo.get_by_id.return_value = courier
    mock_courier_repo.update = AsyncMock()

    handler = MoveCouriersHandler(
        order_repository=mock_order_repo,
        courier_repository=mock_courier_repo
    )

    await handler.handle(MoveCouriersCommand())

    assert courier.location == order.location
    assert order.status == OrderStatus.COMPLETED
    assert courier.status == CourierStatus.FREE
    assert mock_order_repo.update.called
    assert mock_courier_repo.update.called

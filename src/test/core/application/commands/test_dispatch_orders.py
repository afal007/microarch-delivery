import pytest
import uuid
from unittest.mock import AsyncMock
from app.core.domain.model.order.order import Order
from app.core.domain.kernel.location import Location
from app.core.domain.model.courier.courier import Courier, TransportParams
from app.core.application.usecases.commands.dispatch_orders import DispatchOrdersCommand, DispatchOrdersHandler


@pytest.mark.asyncio
async def test_dispatch_orders_success():
    order = Order.create_new(id=uuid.uuid4(), location=Location(x=3, y=3))
    courier = Courier.create(
        name="Anna",
        transport_params=TransportParams(name="bike", speed=2),
        location=Location(x=1, y=1)
    )

    mock_order_repo = AsyncMock()
    mock_order_repo.get_all_new.return_value = [order]
    mock_order_repo.update = AsyncMock()

    mock_courier_repo = AsyncMock()
    mock_courier_repo.get_all_free.return_value = [courier]
    mock_courier_repo.update = AsyncMock()

    mock_dispatch_service = AsyncMock()
    mock_dispatch_service.dispatch.return_value = courier

    handler = DispatchOrdersHandler(
        dispatch_service=mock_dispatch_service,
        order_repository=mock_order_repo,
        courier_repository=mock_courier_repo
    )

    await handler.handle(DispatchOrdersCommand())

    mock_order_repo.update.assert_called_once_with(order)
    mock_courier_repo.update.assert_called_once_with(courier)


@pytest.mark.asyncio
async def test_dispatch_orders_no_orders():
    mock_order_repo = AsyncMock()
    mock_order_repo.get_all_new.return_value = []

    handler = DispatchOrdersHandler(
        dispatch_service=AsyncMock(),
        order_repository=mock_order_repo,
        courier_repository=AsyncMock()
    )

    await handler.handle(DispatchOrdersCommand())
    mock_order_repo.update.assert_not_called()


@pytest.mark.asyncio
async def test_dispatch_orders_no_dispatch_result():
    order = Order.create_new(id=uuid.uuid4(), location=Location(x=3, y=3))
    courier = Courier.create(
        name="Ben",
        transport_params=TransportParams(name="car", speed=3),
        location=Location(x=2, y=2)
    )

    mock_order_repo = AsyncMock()
    mock_order_repo.get_all_new.return_value = [order]
    mock_order_repo.update = AsyncMock()

    mock_courier_repo = AsyncMock()
    mock_courier_repo.get_all_free.return_value = [courier]
    mock_courier_repo.update = AsyncMock()

    mock_dispatch_service = AsyncMock()
    mock_dispatch_service.dispatch.return_value = None

    handler = DispatchOrdersHandler(
        dispatch_service=mock_dispatch_service,
        order_repository=mock_order_repo,
        courier_repository=mock_courier_repo
    )

    await handler.handle(DispatchOrdersCommand())

    mock_order_repo.update.assert_not_called()
    mock_courier_repo.update.assert_not_called()

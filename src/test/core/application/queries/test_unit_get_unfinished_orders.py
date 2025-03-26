import pytest
import uuid
from unittest.mock import AsyncMock
from app.core.domain.kernel.location import Location
from app.core.domain.model.order.order import Order
from app.core.application.usecases.queries.get_unfinished_orders import (
    GetUnfinishedOrdersHandler,
    GetUnfinishedOrdersQuery,
    OrderDTO
)


@pytest.mark.asyncio
async def test_get_unfinished_orders_handler_returns_all():
    order1 = Order.create_new(id=uuid.uuid4(), location=Location(x=1, y=1))
    order2 = Order.create_new(id=uuid.uuid4(), location=Location(x=2, y=2))
    order2.assign_courier(uuid.uuid4())

    mock_repo = AsyncMock()
    mock_repo.get_all_new.return_value = [order1]
    mock_repo.get_all_assigned.return_value = [order2]

    handler = GetUnfinishedOrdersHandler(order_repository=mock_repo)
    result = await handler.handle(GetUnfinishedOrdersQuery())

    assert len(result) == 2

    assert result[0].id == order1.id
    assert result[0].location.x == order1.location.x
    assert result[0].location.y == order1.location.y

    assert result[1].id == order2.id
    assert result[1].location.x == order2.location.x
    assert result[1].location.y == order2.location.y

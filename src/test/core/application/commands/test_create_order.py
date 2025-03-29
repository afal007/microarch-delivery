import uuid
import pytest
from unittest.mock import AsyncMock
from app.core.domain.model.order.order import Order, OrderStatus
from app.core.application.usecases.commands.create_order import CreateOrderCommand, CreateOrderHandler


@pytest.mark.asyncio
async def test_create_order_command():
    # Arrange
    mock_repo = AsyncMock()
    handler = CreateOrderHandler(order_repository=mock_repo)
    command = CreateOrderCommand(order_id=uuid.uuid4(), street="Some Street")

    # Act
    await handler.handle(command)

    # Assert
    assert mock_repo.add.called
    added_order = mock_repo.add.call_args[0][0]
    assert isinstance(added_order, Order)
    assert added_order.status == OrderStatus.CREATED
    assert added_order.id == command.order_id

import pytest
from unittest.mock import AsyncMock
from app.core.application.usecases.queries.get_all_couriers import (
    GetAllCouriersHandler,
    GetAllCouriersQuery,
    CourierDTO
)
from app.core.domain.kernel.location import Location
from app.core.domain.model.courier.courier import Courier, TransportParams


@pytest.mark.asyncio
async def test_get_all_couriers_handler():
    courier1 = Courier.create(
        name="Alex",
        transport_params=TransportParams(name="bike", speed=2),
        location=Location(x=1, y=1)
    )
    courier2 = Courier.create(
        name="Lena",
        transport_params=TransportParams(name="car", speed=3),
        location=Location(x=5, y=7)
    )

    mock_repo = AsyncMock()
    mock_repo.get_all.return_value = [courier1, courier2]

    handler = GetAllCouriersHandler(courier_repository=mock_repo)
    result = await handler.handle(GetAllCouriersQuery())

    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], CourierDTO)

    assert result[0].id == courier1.id
    assert result[0].name == courier1.name
    assert result[0].location.x == courier1.location.x
    assert result[0].location.y == courier1.location.y

    assert result[1].id == courier2.id
    assert result[1].name == courier2.name
    assert result[1].location.x == courier2.location.x
    assert result[1].location.y == courier2.location.y

import pytest
from uuid import uuid4
from app.core.domain.kernel.location import Location
from app.core.domain.model.courier.transport import Transport
from app.core.domain.model.order.order import Order, OrderStatus
from app.core.domain.model.courier.courier import Courier, CourierStatus
from app.core.domain.services.dispatch_service import DispatchService


def test_dispatch_success():
    transport1 = Transport(name="Bike", speed=2)
    transport2 = Transport(name="Car", speed=3)

    courier1 = Courier.create(name="Courier1", transport=transport1, location=Location(x=1, y=1))
    courier2 = Courier.create(name="Courier2", transport=transport2, location=Location(x=2, y=1))

    order = Order.create_new(id=uuid4(), location=Location(x=1, y=10))

    service = DispatchService()
    assigned_courier = service.dispatch(order, [courier1, courier2])

    assert assigned_courier == courier2
    assert order.status == OrderStatus.ASSIGNED
    assert order.courier_id == assigned_courier.id
    assert assigned_courier.status == CourierStatus.BUSY


def test_dispatch_no_free_couriers():
    transport1 = Transport(name="Bike", speed=2)
    transport2 = Transport(name="Car", speed=3)

    courier1 = Courier.create(name="Courier1", transport=transport1, location=Location(x=1, y=1))
    courier2 = Courier.create(name="Courier2", transport=transport2, location=Location(x=2, y=1))

    courier1.set_status_busy()
    courier2.set_status_busy()

    order = Order.create_new(id=uuid4(), location=Location(x=3, y=3))

    service = DispatchService()
    assigned_courier_id = service.dispatch(order, [courier1, courier2])

    assert assigned_courier_id is None  # No available couriers
    assert order.status == OrderStatus.CREATED  # Order remains unassigned
    assert order.courier_id is None


def test_dispatch_invalid_order_status():
    transport = Transport(name="Bike", speed=2)
    courier = Courier.create(name="Courier1", transport=transport, location=Location(x=1, y=1))

    order = Order.create_new(id=uuid4(), location=Location(x=3, y=3))
    order.assign_courier(uuid4())  # Manually assign to make status invalid

    service = DispatchService()

    with pytest.raises(ValueError, match="Order must be in CREATED status to be dispatched."):
        service.dispatch(order, [courier])  # Should fail due to invalid order status

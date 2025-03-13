import pytest
from uuid import uuid4
from app.core.domain.kernel.location import Location
from app.core.domain.model.order.order import Order, OrderStatus


def test_order_creation():
    order_id = uuid4()
    location = Location(x=5, y=5)
    order = Order.create_new(id=order_id, location=location)

    assert order.id == order_id
    assert order.location == location
    assert order.status == OrderStatus.CREATED
    assert order.courier_id is None


def test_order_assign_courier():
    order_id = uuid4()
    location = Location(x=5, y=5)
    courier_id = uuid4()
    order = Order.create_new(id=order_id, location=location)

    order.assign_courier(courier_id)

    assert order.status == OrderStatus.ASSIGNED
    assert order.courier_id == courier_id


def test_order_assign_courier_invalid_status():
    order_id = uuid4()
    location = Location(x=5, y=5)
    courier_id = uuid4()
    order = Order.create_new(id=order_id, location=location)

    order.assign_courier(courier_id)
    with pytest.raises(ValueError, match="Order can only be assigned if it is in CREATED status"):
        order.assign_courier(uuid4())  # Attempting to reassign should fail


def test_order_complete():
    order_id = uuid4()
    location = Location(x=5, y=5)
    courier_id = uuid4()
    order = Order.create_new(id=order_id, location=location)

    order.assign_courier(courier_id)
    order.complete()

    assert order.status == OrderStatus.COMPLETED


def test_order_complete_invalid_status():
    order_id = uuid4()
    location = Location(x=5, y=5)
    order = Order.create_new(id=order_id, location=location)

    with pytest.raises(ValueError, match="Only assigned orders can be completed"):
        order.complete()  # Completing an unassigned order should fail


def test_order_private_constructor():
    with pytest.raises(RuntimeError, match="Please use named constructors!"):
        Order(_create_key="string", _id=uuid4(), _status=OrderStatus.ASSIGNED, _location=Location(x=1, y=2),
              _courier_id=uuid4())

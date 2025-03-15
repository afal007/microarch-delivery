import pytest
from uuid import uuid4
from app.core.domain.kernel.location import Location
from app.core.domain.model.courier.courier import Courier, CourierStatus, TransportParams


def test_courier_creation():
    transport = TransportParams(name="Bike", speed=2)
    location = Location(x=5, y=5)
    courier = Courier.create(name="John", transport_params=transport, location=location)

    assert courier.name == "John"
    assert courier.transport.name == transport.name
    assert courier.transport.speed == transport.speed
    assert courier.location == location
    assert courier.status == CourierStatus.FREE
    assert isinstance(courier.id, uuid4().__class__)  # Ensure ID is a UUID


def test_courier_set_status_busy():
    transport = TransportParams(name="Bike", speed=2)
    location = Location(x=5, y=5)
    courier = Courier.create(name="John", transport_params=transport, location=location)

    courier.set_status_busy()
    assert courier.name == "John"
    assert courier.transport.name == transport.name
    assert courier.transport.speed == transport.speed
    assert courier.location == location
    assert courier.status == CourierStatus.BUSY
    assert isinstance(courier.id, uuid4().__class__)  # Ensure ID is a UUID


def test_courier_set_status_busy_invalid():
    transport = TransportParams(name="Bike", speed=2)
    location = Location(x=5, y=5)
    courier = Courier.create(name="John", transport_params=transport, location=location)

    courier.set_status_busy()
    with pytest.raises(ValueError, match="Courier can only be set to busy if currently free"):
        courier.set_status_busy()  # Should fail because already busy


def test_courier_set_status_free():
    transport = TransportParams(name="Bike", speed=2)
    location = Location(x=5, y=5)
    courier = Courier.create(name="John", transport_params=transport, location=location)

    courier.set_status_busy()
    courier.set_status_free()

    assert courier.name == "John"
    assert courier.transport.name == transport.name
    assert courier.transport.speed == transport.speed
    assert courier.location == location
    assert courier.status == CourierStatus.FREE
    assert isinstance(courier.id, uuid4().__class__)  # Ensure ID is a UUID


def test_courier_set_status_free_invalid():
    transport = TransportParams(name="Bike", speed=2)
    location = Location(x=5, y=5)
    courier = Courier.create(name="John", transport_params=transport, location=location)

    with pytest.raises(ValueError, match="Courier can only be set to free if currently busy"):
        courier.set_status_free()  # Should fail because not busy


def test_courier_steps_to_order():
    transport = TransportParams(name="Bike", speed=2)
    courier_location = Location(x=1, y=1)
    order_location = Location(x=5, y=5)
    courier = Courier.create(name="John", transport_params=transport, location=courier_location)

    steps = courier.steps_to_order(order_location)
    assert steps == 4  # Distance is 8 cells, speed is 2, so 8 / 2 = 4 steps


def test_courier_movement_towards_order():
    transport = TransportParams(name="Bike", speed=2)
    courier_location = Location(x=1, y=1)
    order_location = Location(x=5, y=5)
    courier = Courier.create(name="John", transport_params=transport, location=courier_location)

    courier.move_towards_order(order_location)
    assert courier.location == Location(x=3, y=1)  # Moves 2 cells closer


def test_courier_private_constructor():
    with pytest.raises(RuntimeError, match="Please use named constructors!"):
        Courier(
            _create_key="string",
            _id=uuid4(),
            _name="Name",
            _transport=TransportParams(name="string", speed=2),
            _location=Location(x=5, y=5),
            _status=CourierStatus.BUSY
        )

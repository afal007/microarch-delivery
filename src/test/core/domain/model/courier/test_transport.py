import pytest
from uuid import uuid4
from app.core.domain.kernel.location import Location
from app.core.domain.model.courier.transport import Transport


def test_transport_creation():
    transport = Transport(name="Bike", speed=2)
    assert transport.name == "Bike"
    assert transport.speed == 2
    assert isinstance(transport.id, uuid4().__class__)  # Ensure ID is a UUID


def test_transport_invalid_name():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Transport(name="", speed=2)  # Name cannot be empty


def test_transport_invalid_speed():
    with pytest.raises(ValueError, match="Speed must be between 1 and 3"):
        Transport(name="Bike", speed=0)  # Speed too low
    with pytest.raises(ValueError, match="Speed must be between 1 and 3"):
        Transport(name="Bike", speed=4)  # Speed too high


def test_transport_equality():
    id_ = uuid4()
    transport1 = Transport(name="Bike", speed=2)
    transport2 = Transport(name="Car", speed=3)
    transport3 = Transport(name="Bike", speed=2)  # Different ID

    assert transport1 != transport2  # Different ID
    assert transport1 != transport3  # Different ID


def test_transport_movement():
    transport = Transport(name="Bike", speed=2)
    current = Location(x=1, y=1)
    target = Location(x=1, y=9)
    new_location = transport.move_towards(current, target)
    assert new_location == Location(x=1, y=3)  # Moves 2 steps towards target

    # Moving diagonally step-by-step
    current = Location(x=1, y=1)
    target = Location(x=5, y=5)
    new_location = transport.move_towards(current, target)
    assert new_location == Location(x=3, y=1)  # Moves 2 cells closer

    # When target is closer than speed
    transport = Transport(name="Bike", speed=3)
    current = Location(x=1, y=1)
    target = Location(x=2, y=2)
    new_location = transport.move_towards(current, target)
    assert new_location == Location(x=2, y=2)  # Should not overshoot


def test_transport_private_fields():
    transport = Transport(name="Bike", speed=2)

    with pytest.raises(AttributeError):
        _ = transport.__id  # Private field should not be accessible

    with pytest.raises(AttributeError):
        _ = transport.__name  # Private field should not be accessible

    with pytest.raises(AttributeError):
        _ = transport.__speed  # Private field should not be accessible


def test_transport_no_setters():
    transport = Transport(name="Bike", speed=2)

    with pytest.raises(AttributeError):
        transport.id = uuid4()

    with pytest.raises(AttributeError):
        transport.name = "Name"

    with pytest.raises(AttributeError):
        transport.speed = 1


def test_transport_constants_immutability():
    Transport.__MIN_SPEED = 0
    Transport.__MAX_SPEED = 10

    # Create a transport object, it should still follow original constants
    with pytest.raises(ValueError, match="Speed must be between 1 and 3"):
        Transport(name="Bike", speed=0)  # Should fail due to unchanged min speed
    with pytest.raises(ValueError, match="Speed must be between 1 and 3"):
        Transport(name="Bike", speed=4)  # Should fail due to unchanged max speed

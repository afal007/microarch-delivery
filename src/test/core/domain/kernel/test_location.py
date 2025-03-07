import pytest

from app.core.domain.kernel.location import Location


def test_location_creation_valid():
    loc = Location(x=5, y=7)
    assert loc.x == 5
    assert loc.y == 7


def test_location_creation_invalid():
    with pytest.raises(ValueError, match="Input should be greater than or equal to 1"):
        Location(x=0, y=5)  # X is below the minimum

    with pytest.raises(ValueError, match="Input should be less than or equal to 10"):
        Location(x=11, y=5)  # X is above the maximum

    with pytest.raises(ValueError, match="Input should be greater than or equal to 1"):
        Location(x=3, y=0)  # Y is below the minimum

    with pytest.raises(ValueError, match="Input should be less than or equal to 10"):
        Location(x=3, y=11)  # Y is above the maximum


def test_location_equality():
    loc1 = Location(x=3, y=4)
    loc2 = Location(x=3, y=4)
    loc3 = Location(x=5, y=6)

    assert loc1 == loc2  # Should be equal
    assert loc1 != loc3  # Should not be equal


def test_distance_calculation():
    loc1 = Location(x=2, y=3)
    loc2 = Location(x=5, y=7)

    assert loc1.distance_to(loc2) == 7  # (|5 - 2| + |7 - 3|) = 3 + 4 = 7

    loc3 = Location(x=1, y=1)
    loc4 = Location(x=10, y=10)

    assert loc3.distance_to(loc4) == 18  # (|10 - 1| + |10 - 1|) = 9 + 9 = 18


def test_random_location():
    loc = Location.random()
    assert 1 <= loc.x <= 10
    assert 1 <= loc.y <= 10


def test_location_immutability():
    loc = Location(x=5, y=5)

    with pytest.raises(ValueError):
        loc.x = 7  # This should raise a TypeError

    with pytest.raises(ValueError):
        loc.y = 3  # This should also raise a TypeError

from pydantic import BaseModel, PrivateAttr
from typing import ClassVar
from uuid import UUID, uuid4
from app.core.domain.kernel.location import Location


class Transport(BaseModel):
    __MIN_SPEED: ClassVar[int] = 1
    __MAX_SPEED: ClassVar[int] = 3

    __id: UUID = PrivateAttr(default_factory=uuid4)  # Private UUID field
    __name: str = PrivateAttr()
    __speed: int = PrivateAttr()

    def __init__(self, name: str, speed: int):
        super().__init__()
        if not (self.__MIN_SPEED <= speed <= self.__MAX_SPEED):
            raise ValueError(f"Speed must be between {self.__MIN_SPEED} and {self.__MAX_SPEED}")
        if not name:
            raise ValueError("Name cannot be empty")

        self.__name = name
        self.__speed = speed

    @property
    def id(self) -> UUID:
        return self.__id  # Expose read-only ID

    @property
    def name(self) -> str:
        return self.__name  # Read-only name

    @property
    def speed(self) -> int:
        return self.__speed  # Read-only speed

    def move_towards(self, current_location: Location, target_location: Location) -> Location:
        dx = target_location.x - current_location.x
        dy = target_location.y - current_location.y

        step_x = min(abs(dx), self.__speed) * (1 if dx > 0 else -1 if dx < 0 else 0)
        step_y = min(abs(dy), self.__speed - abs(step_x)) * (1 if dy > 0 else -1 if dy < 0 else 0)

        new_x = current_location.x + step_x
        new_y = current_location.y + step_y

        return Location(x=new_x, y=new_y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transport):
            return False
        return self.__id == other.__id

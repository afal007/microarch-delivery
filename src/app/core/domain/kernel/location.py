from pydantic import BaseModel, ConfigDict, Field
import random


class Location(BaseModel):
    model_config = ConfigDict(frozen=True)

    x: int = Field(..., ge=1, le=10)
    y: int = Field(..., ge=1, le=10)

    def distance_to(self, other: "Location") -> int:
        """
        Calculate the Manhattan distance between two locations.
        """
        if not isinstance(other, Location):
            raise TypeError("Argument must be a Location instance")

        return abs(self.x - other.x) + abs(self.y - other.y)

    @classmethod
    def random(cls) -> "Location":
        """
        Generate a random valid location.
        """
        return cls(
            x=random.randint(1, 10),
            y=random.randint(1, 10)
        )

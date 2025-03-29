from abc import ABC, abstractmethod

from app.core.domain.kernel import Location


class IGeoClient(ABC):
    @abstractmethod
    async def get_geolocation(self, street: str) -> Location:
        pass

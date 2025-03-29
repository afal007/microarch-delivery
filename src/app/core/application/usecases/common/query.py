from abc import ABC, abstractmethod


class Query(ABC):
    pass


class IQueryHandler(ABC):
    @abstractmethod
    async def handle(self, query: object) -> object:
        pass

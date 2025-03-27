from abc import ABC, abstractmethod


class Command(ABC):
    pass


class ICommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: Command) -> None:
        pass

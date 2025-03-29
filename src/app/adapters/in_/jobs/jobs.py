import logging
from abc import ABC, abstractmethod

from app.core.application.usecases.commands.dispatch_orders import DispatchOrdersCommand, IDispatchOrdersHandler
from app.core.application.usecases.commands.move_couriers import IMoveCouriersHandler, MoveCouriersCommand

logger = logging.getLogger(__name__)


# Marker base class
class Job(ABC):
    @abstractmethod
    async def run(self):
        pass


class MoveCouriersJob(Job):
    def __init__(self, handler: IMoveCouriersHandler):
        self._handler = handler

    async def run(self):
        logger.info("Running MoveCouriersJob")
        try:
            await self._handler.handle(MoveCouriersCommand())
            logger.info("MoveCouriersJob completed successfully")
        except Exception as e:
            logger.exception(f"MoveCouriersJob failed: {e}")


class DispatchOrdersJob(Job):
    def __init__(self, handler: IDispatchOrdersHandler):
        self._handler = handler

    async def run(self):
        logger.info("Running DispatchOrdersJob")
        try:
            await self._handler.handle(DispatchOrdersCommand())
            logger.info("DispatchOrdersJob completed successfully")
        except Exception as e:
            logger.exception(f"DispatchOrdersJob failed: {e}")

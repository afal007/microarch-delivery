from abc import abstractmethod

from app.core.application.usecases.common.command import Command, ICommandHandler
from app.core.domain.services.dispatch_service import IDispatchService
from app.core.ports.i_courier_repository import ICourierRepository
from app.core.ports.i_order_repository import IOrderRepository


class DispatchOrdersCommand(Command):
    pass


class IDispatchOrdersHandler(ICommandHandler):
    @abstractmethod
    async def handle(self, command: DispatchOrdersCommand) -> None:
        pass


class DispatchOrdersHandler(IDispatchOrdersHandler):
    def __init__(self,
                 dispatch_service: IDispatchService,
                 order_repository: IOrderRepository,
                 courier_repository: ICourierRepository
                 ):
        self._dispatch_service = dispatch_service
        self._order_repository = order_repository
        self._courier_repository = courier_repository

    async def handle(self, command: DispatchOrdersCommand) -> None:
        orders = await self._order_repository.get_all_new()
        couriers = await self._courier_repository.get_all_free()

        if not orders or not couriers:
            return

        order = orders[0]  # взять первый заказ
        courier = await self._dispatch_service.dispatch(order, couriers)

        # TODO: Unit Of Work для транзакционности
        if courier:
            await self._order_repository.update(order)
            await self._courier_repository.update(courier)

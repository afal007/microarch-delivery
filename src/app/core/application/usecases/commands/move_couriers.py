from abc import abstractmethod

from app.core.application.usecases.common.command import Command, ICommandHandler
from app.core.ports.i_courier_repository import ICourierRepository
from app.core.ports.i_order_repository import IOrderRepository


class MoveCouriersCommand(Command):
    pass


class IMoveCouriersHandler(ICommandHandler):
    @abstractmethod
    async def handle(self, command: MoveCouriersCommand) -> None:
        pass


class MoveCouriersHandler(IMoveCouriersHandler):
    def __init__(self, order_repository: IOrderRepository, courier_repository: ICourierRepository):
        self._order_repository = order_repository
        self._courier_repository = courier_repository

    async def handle(self, command: MoveCouriersCommand) -> None:
        assigned_orders = await self._order_repository.get_all_assigned()

        for order in assigned_orders:
            courier = await self._courier_repository.get_by_id(order.courier_id)
            if courier is None:
                continue

            # Move courier toward the order's location
            courier.move_towards_order(order.location)

            if courier.location == order.location:
                order.complete()
                courier.set_status_free()

                await self._order_repository.update(order)
                await self._courier_repository.update(courier)
            else:
                await self._courier_repository.update(courier)

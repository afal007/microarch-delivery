from dishka import Provider, Scope, provide

from adapters.out.postgresql.order.test_order_repository import order_repository
from app.core.application.usecases.commands.create_order import CreateOrderHandler, ICreateOrderHandler
from app.core.application.usecases.commands.dispatch_orders import DispatchOrdersHandler, IDispatchOrdersHandler
from app.core.application.usecases.commands.move_couriers import IMoveCouriersHandler, MoveCouriersHandler
from app.core.application.usecases.queries.get_all_couriers import GetAllCouriersHandler, IGetAllCouriersHandler
from app.core.application.usecases.queries.get_unfinished_orders import GetUnfinishedOrdersHandler, \
    IGetUnfinishedOrdersHandler
from app.core.domain.services.i_dispatch_service import IDispatchService
from app.core.ports.i_courier_repository import ICourierRepository
from app.core.ports.i_order_repository import IOrderRepository


class HandlersProvider(Provider):
    @provide(scope=Scope.APP)
    def get_create_order_handler(self, order_repository: IOrderRepository) -> ICreateOrderHandler:
        return CreateOrderHandler(order_repository)

    @provide(scope=Scope.APP)
    def get_dispatch_orders_handler(self,
                                    dispatch_service: IDispatchService,
                                    order_repository: IOrderRepository,
                                    courier_repository: ICourierRepository,
                                    ) -> IDispatchOrdersHandler:
        return DispatchOrdersHandler(dispatch_service, order_repository, courier_repository)

    @provide(scope=Scope.APP)
    def get_move_couriers_handler(self,
                                  order_repository: IOrderRepository,
                                  courier_repository: ICourierRepository,
                                  ) -> IMoveCouriersHandler:
        return MoveCouriersHandler(order_repository, courier_repository)

    @provide(scope=Scope.APP)
    def get_all_couriers_handler(self, courier_repository: ICourierRepository) -> IGetAllCouriersHandler:
        return GetAllCouriersHandler(courier_repository)

    @provide(scope=Scope.APP)
    def get_unfinished_orders_handler(self, order_repository: IOrderRepository) -> IGetUnfinishedOrdersHandler:
        return GetUnfinishedOrdersHandler(order_repository)

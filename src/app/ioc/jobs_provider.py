from dishka import Provider, Scope, provide

from app.adapters.in_.jobs.jobs import DispatchOrdersJob, MoveCouriersJob
from app.core.application.usecases.commands.dispatch_orders import IDispatchOrdersHandler
from app.core.application.usecases.commands.move_couriers import IMoveCouriersHandler


class JobsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_move_couriers_job(self, handler: IMoveCouriersHandler) -> MoveCouriersJob:
        return MoveCouriersJob(handler)

    @provide(scope=Scope.APP)
    def get_dispatch_orders_job(self, handler: IDispatchOrdersHandler) -> DispatchOrdersJob:
        return DispatchOrdersJob(handler)

from dishka import Provider, provide, Scope

from app.core.domain.services.dispatch_service import DispatchService
from app.core.domain.services.i_dispatch_service import IDispatchService


class DispatchServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_dispatch_service(self) -> IDispatchService:
        return DispatchService()

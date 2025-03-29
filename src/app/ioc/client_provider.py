from dishka import Provider, Scope, provide
from dynaconf import Dynaconf

from app.adapters.out.grpc.geo.client import GeoClient
from app.core.ports.geo_client import IGeoClient


class ClientProvider(Provider):
    @provide(scope=Scope.APP)
    def get_geo_client(self, config: Dynaconf) -> IGeoClient:
        return GeoClient(config.geo.url)

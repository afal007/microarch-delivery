import grpc

from app.core.domain.kernel import Location
from app.core.ports.geo_client import IGeoClient
from .geo_pb2 import GetGeolocationRequest
from .geo_pb2_grpc import GeoStub


class GeoClient(IGeoClient):
    def __init__(self, address: str):
        self._address = address
        self._channel: grpc.aio.Channel | None = None
        self._stub: GeoStub | None = None

    async def __aenter__(self):
        self._channel = grpc.aio.insecure_channel(self._address)
        self._stub = GeoStub(self._channel)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._channel:
            await self._channel.close()

    async def connect(self):
        self._channel = grpc.aio.insecure_channel(self._address)
        self._stub = GeoStub(self._channel)

    async def close(self):
        if self._channel:
            await self._channel.close()

    async def get_geolocation(self, street: str) -> Location:
        await self.connect()
        request = GetGeolocationRequest(Street=street)
        response = await self._stub.GetGeolocation(request)
        await self.close()
        return Location(x=response.Location.x, y=response.Location.y)

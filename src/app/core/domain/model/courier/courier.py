from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, PrivateAttr
from app.core.domain.kernel.location import Location
from app.core.domain.model.courier.transport import Transport


class CourierStatus(str, Enum):
    FREE = "free"
    BUSY = "busy"


class TransportParams(BaseModel):
    name: str
    speed: int


class Courier(BaseModel):
    __create_key = object()

    __id: UUID = PrivateAttr()
    __name: str = PrivateAttr()
    __transport: Transport = PrivateAttr()
    __location: Location = PrivateAttr()
    __status: CourierStatus = PrivateAttr()

    def __init__(self, _create_key, _id, _name, _transport, _location, _status):
        if _create_key != Courier.__create_key:
            raise RuntimeError("Please use named constructors!")

        super().__init__()
        self.__id = _id
        self.__name = _name
        self.__transport = _transport
        self.__location = _location
        self.__status = _status

    @classmethod
    def create(cls, name: str, transport_params: TransportParams, location: Location) -> "Courier":
        """Factory method to create a courier with default status and a managed transport entity."""
        return cls(
            _create_key=cls.__create_key,
            _id=uuid4(),
            _name=name,
            _transport=Transport(**transport_params.model_dump()),
            _location=location,
            _status=CourierStatus.FREE
        )

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def transport(self) -> Transport:
        return self.__transport

    @property
    def location(self) -> Location:
        return self.__location

    @property
    def status(self) -> CourierStatus:
        return self.__status

    def set_status_busy(self):
        if self.status != CourierStatus.FREE:
            raise ValueError("Courier can only be set to busy if currently free")

        self.__status = CourierStatus.BUSY

    def set_status_free(self):
        if self.status != CourierStatus.BUSY:
            raise ValueError("Courier can only be set to free if currently busy")

        self.__status = CourierStatus.FREE

    def steps_to_order(self, order_location: Location) -> int:
        """Calculate the number of steps required to reach the order location."""
        distance = self.__location.distance_to(order_location)
        return (distance + self.__transport.speed - 1) // self.__transport.speed  # Ceiling division

    def move_towards_order(self, order_location: Location):
        """Move one step towards the order's location using Transport's move method."""
        self.__location = self.__transport.move_towards(self.__location, order_location)

from pydantic import BaseModel, PrivateAttr
from uuid import UUID

from app.core.domain.kernel.location import Location
from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "created"
    ASSIGNED = "assigned"
    COMPLETED = "completed"


class Order(BaseModel):
    __create_key = object()

    __id: UUID = PrivateAttr()
    __location: Location = PrivateAttr()
    __status: OrderStatus = PrivateAttr()
    __courier_id: UUID | None = PrivateAttr()

    def __init__(self, _create_key, _id, _location, _status, _courier_id):
        if _create_key != Order.__create_key:
            raise RuntimeError("Please use named constructors!")

        super().__init__()
        self.__id = _id
        self.__status = _status
        self.__location = _location
        self.__courier_id = _courier_id

    @classmethod
    def restore(cls, id: UUID, location_x: int, location_y: int, status: str, courier_id: UUID) -> "Order":
        """Factory method to restore an order from """
        return cls(
            _create_key=cls.__create_key,
            _id=id,
            _location=Location(x=location_x, y=location_y),
            _status=OrderStatus(status),
            _courier_id=courier_id
        )

    @classmethod
    def create_new(cls, id: UUID, location: Location) -> "Order":
        """Factory method to create an order with default status."""
        return cls(
            _create_key=cls.__create_key,
            _id=id,
            _location=location,
            _status=OrderStatus.CREATED,
            _courier_id=None
        )

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def location(self) -> Location:
        return self.__location

    @property
    def status(self) -> OrderStatus:
        return self.__status

    @property
    def courier_id(self) -> UUID | None:
        return self.__courier_id

    def assign_courier(self, courier_id: UUID):
        if self.status != OrderStatus.CREATED:
            raise ValueError("Order can only be assigned if it is in CREATED status")
        self.__status = OrderStatus.ASSIGNED
        self.__courier_id = courier_id

    def complete(self):
        if self.status != OrderStatus.ASSIGNED:
            raise ValueError("Only assigned orders can be completed")
        self.__status = OrderStatus.COMPLETED

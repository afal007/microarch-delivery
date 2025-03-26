from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base, relationship

from app.core.domain.model.courier.courier import Courier
from app.adapters.out.postgresql.courier.transport_db import TransportDB
from app.core.domain.model.courier.transport import Transport

Base = declarative_base()


class CourierDB(Base):
    __tablename__ = "couriers"

    id = Column(PGUUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    transport_id = Column(PGUUID(as_uuid=True), ForeignKey(TransportDB.id), nullable=False)
    location_x = Column(Integer, nullable=False)
    location_y = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    transport = relationship(TransportDB, lazy="joined")

    @classmethod
    def from_domain(cls, courier: Courier) -> "CourierDB":
        return cls(
            id=courier.id,
            name=courier.name,
            transport_id=courier.transport.id,
            location_x=courier.location.x,
            location_y=courier.location.y,
            status=courier.status.value
        )

    def update_from_domain(self, courier: Courier) -> "CourierDB":
        self.id = courier.id
        self.name = courier.name
        self.transport_id = courier.transport.id
        self.transport = self.transport.update_from_domain(courier.transport)
        self.location_x = courier.location.x
        self.location_y = courier.location.y
        self.status = courier.status.value
        return self

    def to_domain(self) -> Courier:
        return Courier.restore(
            id=self.id,
            name=self.name,
            status=self.status,
            transport=Transport(name=self.transport.name, speed=self.transport.speed),
            location_x=self.location_x, location_y=self.location_y
        )

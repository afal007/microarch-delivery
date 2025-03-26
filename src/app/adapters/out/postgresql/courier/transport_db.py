from uuid import UUID
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base
from app.core.domain.model.courier.transport import Transport

Base = declarative_base()


class TransportDB(Base):
    __tablename__ = "transports"

    id = Column(PGUUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    speed = Column(Integer, nullable=False)

    def to_domain(self) -> Transport:
        return Transport(name=self.name, speed=self.speed)

    @classmethod
    def from_domain(cls, transport: Transport) -> "TransportDB":
        return cls(
            id=transport.id,
            name=transport.name,
            speed=transport.speed
        )

    def update_from_domain(self, transport: Transport) -> "TransportDB":
        self.id = transport.id
        self.name = transport.name
        self.speed = transport.speed
        return self

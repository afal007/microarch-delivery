from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base
from app.core.domain.model.order.order import Order

Base = declarative_base()


class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(PGUUID(as_uuid=True), primary_key=True)
    location_x = Column(Integer, nullable=False)
    location_y = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    courier_id = Column(PGUUID(as_uuid=True), nullable=True)

    @classmethod
    def from_domain(cls, order: Order) -> "OrderDB":
        return (cls(
            id=order.id,
            location_x=order.location.x,
            location_y=order.location.y,
            status=order.status,
            courier_id=order.courier_id
        ))

    def update_from_domain(self, order: Order) -> "OrderDB":
        self.id = order.id
        self.location_x = order.location.x
        self.location_y = order.location.y
        self.status = order.status
        self.courier_id = order.courier_id
        return self

    def to_domain(self) -> Order:
        return Order.restore(
            id=self.id,
            location_x=self.location_x,
            location_y=self.location_y,
            status=self.status,
            courier_id=self.courier_id
        )

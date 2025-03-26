from uuid import uuid4, UUID
from fastapi import APIRouter, FastAPI
from dynaconf import Dynaconf
from dishka.integrations.fastapi import FromDishka, DishkaRoute, setup_dishka
from pydantic import BaseModel, PrivateAttr
from app.core.domain.kernel import Location
from app.core.domain.model.courier.courier import TransportParams, Courier, CourierStatus
from app.core.domain.model.order.order import Order
from app.core.domain.services.i_dispatch_service import IDispatchService
from app.core.ports.i_order_repository import IOrderRepository
from app.ioc.composition_root import container

router = APIRouter(route_class=DishkaRoute)


class TransportDTO(BaseModel):
    id: UUID
    name: str
    speed: int


class LocationDTO(BaseModel):
    x: int
    y: int


class CourierDTO(BaseModel):
    id: UUID
    name: str
    transport: TransportDTO
    location: LocationDTO
    status: CourierStatus


@router.post("/courier:dispatch", tags=["Courier"], )
async def dispatch_courier(
        dispatch_service: FromDishka[IDispatchService],
        order_repository: FromDishka[IOrderRepository],
) -> CourierDTO | None:
    transport1 = TransportParams(name="Bike", speed=2)
    transport2 = TransportParams(name="Car", speed=3)

    courier1 = Courier.create(name="Courier1", transport_params=transport1, location=Location(x=1, y=1))
    courier2 = Courier.create(name="Courier2", transport_params=transport2, location=Location(x=2, y=1))

    order = await order_repository.get_by_id(uuid4())
    # Order.create_new(id=uuid4(), location=Location(x=2, y=10)))

    courier_ = await dispatch_service.dispatch(order, [courier1, courier2])
    return CourierDTO(
        id=courier_.id
        , name=courier_.name
        , transport=TransportDTO(**courier_.transport.model_dump())
        , location=LocationDTO(**courier_.location.model_dump())
        , status=courier_.status
    )


@router.get("/config", tags=["Config"], )
async def get_config(
        config: FromDishka[Dynaconf],
) -> str | None:
    print(config)
    print(config.postgres)
    return ''


app = FastAPI()
app.include_router(router)
setup_dishka(container, app)

import uuid
from typing import List

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from app.adapters.in_.http.models.error import ErrorDTO
from app.core.application.usecases.commands.create_order import CreateOrderCommand, ICreateOrderHandler
from app.core.application.usecases.queries.get_unfinished_orders import GetUnfinishedOrdersQuery, \
    IGetUnfinishedOrdersHandler, OrderDTO

order_router = APIRouter(route_class=DishkaRoute)


@order_router.post(
    "/api/v1/orders",
    responses={
        201: {"description": "Успешный ответ"},
        500: {"model": ErrorDTO, "description": "Ошибка"},
    },
    tags=["Orders"],
    summary="Создать заказ",
    response_model_by_alias=True,
)
async def create_order(handler: FromDishka[ICreateOrderHandler]) -> None:
    """Позволяет создать заказ с целью тестирования"""
    await handler.handle(CreateOrderCommand(order_id=uuid.uuid4(), street="Ignored"))
    return


@order_router.get(
    "/api/v1/orders/active",
    responses={
        200: {"model": List[OrderDTO], "description": "Успешный ответ"},
        500: {"model": ErrorDTO, "description": "Ошибка"},
    },
    tags=["Orders"],
    summary="Получить все незавершенные заказы",
    response_model_by_alias=True,
)
async def get_orders(handler: FromDishka[IGetUnfinishedOrdersHandler]) -> List[OrderDTO]:
    """Позволяет получить все незавершенные"""
    return await handler.handle(GetUnfinishedOrdersQuery())

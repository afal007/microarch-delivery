from typing import List

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from app.adapters.in_.http.models.courier import CourierDTO
from app.adapters.in_.http.models.error import ErrorDTO
from app.core.application.usecases.queries.get_all_couriers import GetAllCouriersQuery, IGetAllCouriersHandler

courier_router = APIRouter(route_class=DishkaRoute)


@courier_router.get(
    "/api/v1/couriers",
    responses={
        200: {"model": List[CourierDTO], "description": "Успешный ответ"},
        500: {"model": ErrorDTO, "description": "Ошибка"},
    },
    tags=["Couriers"],
    summary="Получить всех курьеров",
    response_model_by_alias=True,
)
async def get_couriers(handler: FromDishka[IGetAllCouriersHandler]) -> List[CourierDTO]:
    """Позволяет получить всех курьеров"""
    return await handler.handle(GetAllCouriersQuery())

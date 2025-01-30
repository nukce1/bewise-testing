from typing import Annotated

from app.dependencies.dependencies import get_application_service
from app.domain.schemas import ApplicationAddDTO, ApplicationFiltersDTO
from app.protocols.applications import ApplicationService
from app.services.exceptions import WrongApplicationDataException
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED,
                              HTTP_500_INTERNAL_SERVER_ERROR)

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", status_code=HTTP_200_OK)
async def get_applications_handler(
    application_filters: Annotated[ApplicationFiltersDTO, Query()],
    application_service: Annotated[
        ApplicationService, Depends(get_application_service)
    ],
):
    """
    Возвращает список заявок с указанными фильтрами.
    Args:
        application_filters: Фильтры для получения заявок
        application_service: Сервис для работы с заявками

    Returns:
        dict: Список заявок
    """
    try:
        return await application_service.get_applications(application_filters)
    except WrongApplicationDataException as exc:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )


@router.post("", status_code=HTTP_201_CREATED)
async def create_application_handler(
    application_data: Annotated[ApplicationAddDTO, Body()],
    application_service: Annotated[
        ApplicationService, Depends(get_application_service)
    ],
):
    """
    Создает заявку пользователя.
    Args:
        application_data: Данные заявки
        application_service: Сервис для работы с заявками

    Returns:
        dict: Идентификатор созданной заявки
    """
    try:
        return await application_service.create_application(application_data)
    except WrongApplicationDataException as exc:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )

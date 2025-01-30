import logging

from app.domain.models import Application
from app.domain.schemas import (ApplicationAddDTO, ApplicationDTO,
                                ApplicationFiltersDTO)
from app.protocols.producer import ProducerService
from app.protocols.storage import Storage
from app.services.exceptions import WrongApplicationDataException
from pydantic import ValidationError


class CustomApplicationService:
    def __init__(self, storage: Storage, producer_service: ProducerService):
        self.storage = storage
        self.producer_service = producer_service

    async def get_applications(
        self, application_filters: ApplicationFiltersDTO
    ) -> dict:
        """
        Возвращает список заявок с указанными фильтрами.
        Args:
            application_filters: Фильтры для получения заявок

        Returns:
            dict: Список заявок
        """
        page: int = application_filters.page
        limit: int = application_filters.limit
        user_name: str | None = application_filters.user_name

        if user_name:
            applications_orm = (
                await self.storage.get_applications_by_username_with_pagination(
                    user_name, page, limit
                )
            )
        else:
            applications_orm = await self.storage.get_applications_with_pagination(
                page, limit
            )

        try:
            serialized_applications = [
                ApplicationDTO.model_validate(app.__dict__) for app in applications_orm
            ]
        except ValidationError as exc:
            logging.error(
                f"Ошибка при преобразовании данных заявок из ORM в DTO - {exc.errors()}"
            )
            raise WrongApplicationDataException(exc.errors())

        applications_list = [app.model_dump() for app in serialized_applications]

        return {"applications": applications_list}

    async def create_application(self, application_data: ApplicationAddDTO) -> dict:
        """
        Создает заявку пользователя.
        Args:
            application_data: Данные заявки

        Returns:
            dict: Идентификатор созданной заявки
        """
        user_name: str = application_data.user_name
        description: str = application_data.description

        created_app: Application = await self.storage.create_application(
            user_name, description
        )

        try:
            created_app_dto = ApplicationDTO.model_validate(created_app.__dict__)
        except ValidationError as exc:
            logging.error(
                f"Ошибка при преобразовании данных заявки из ORM в DTO - {exc.errors()}"
            )
            raise WrongApplicationDataException(exc.errors())

        await self.producer_service.send_application_created(created_app_dto)
        logging.info(f"Созданная заявка {created_app.id} успешно доставлена брокеру.")

        return {"id": str(created_app.id)}

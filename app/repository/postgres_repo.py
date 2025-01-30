import logging

from app.domain.models import Application
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresStorage:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_applications_by_username_with_pagination(
        self, user_name: str, page: int, limit: int
    ) -> list[Application]:
        """
        Возвращает список заявок пользователя согласно пагинации.
        Args:
            user_name: Имя пользователя
            page: Номер страницы
            limit: Количество записей на странице

        Returns
            list[Application]: Список заявок пользователя
        """
        offset: int = (page - 1) * limit
        query = (
            select(Application)
            .filter_by(user_name=user_name)
            .order_by(Application.id)
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)

        applications_orm = list(result.scalars().all())

        return applications_orm

    async def get_applications_with_pagination(
        self, page: int, limit: int
    ) -> list[Application]:
        """
        Возвращает список всех заявок согласно пагинации.
        Args:
            page: Номер страницы
            limit: Количество записей на странице

        Returns
            list[Application]: Список заявок
        """
        offset: int = (page - 1) * limit
        query = select(Application).order_by(Application.id).offset(offset).limit(limit)

        result = await self.session.execute(query)

        applications_orm = list(result.scalars().all())

        return applications_orm

    async def create_application(self, user_name: str, description: str) -> Application:
        """
        Создает заявку пользователя.
        Args:
            user_name: Имя пользователя
            description: Описание заявки

        Returns:
            Application: ORM объект созданной заявки
        """
        application_orm = Application(user_name=user_name, description=description)

        self.session.add(application_orm)

        await self.session.commit()
        await self.session.refresh(application_orm)

        logging.info(
            f"Заявка {application_orm.id} пользователя {user_name} успешно создана."
        )

        return application_orm

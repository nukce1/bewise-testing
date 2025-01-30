import pytest
from app.domain.models import Application
from app.repository.postgres_repo import PostgresStorage
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_application(session: AsyncSession, application_add_data_dto):
    user_name: str = application_add_data_dto.user_name
    description: str = application_add_data_dto.description

    storage = PostgresStorage(session)
    created_app: Application = await storage.create_application(user_name, description)

    assert created_app.id == 1
    assert created_app.user_name == user_name
    assert created_app.description == description



@pytest.mark.asyncio
async def test_get_applications_by_username_with_pagination(
    session: AsyncSession, applications_add_data_dict, application_filters_dto_data
):
    applications_orm = [
        Application(**data) for data in applications_add_data_dict
    ]
    session.add_all(applications_orm)

    await session.flush()

    storage = PostgresStorage(session)
    username: str = application_filters_dto_data.user_name
    page: int = application_filters_dto_data.page
    limit: int = application_filters_dto_data.limit

    result: list[Application] = await storage.get_applications_by_username_with_pagination(
        username, page, limit
    )

    assert len(result) == 2
    assert result[0].__dict__ == applications_orm[0].__dict__
    assert result[1].__dict__ == applications_orm[1].__dict__

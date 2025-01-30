from unittest.mock import Mock

import pytest
from app.domain.models import Application
from app.repository.postgres_repo import PostgresStorage
from app.services.application_service import CustomApplicationService


@pytest.mark.asyncio
async def test_get_applications(
    monkeypatch,
    applications_created_data_dto,
    applications_created_data_dict,
    application_filters_without_username_dto_data,
):

    async def mock_get_applications_with_pagination(
        self, page: int, limit: int
    ) -> list[Application]:
        return [
            Application(**app.model_dump()) for app in applications_created_data_dto
        ]

    monkeypatch.setattr(
        PostgresStorage,
        "get_applications_with_pagination",
        mock_get_applications_with_pagination,
    )

    application_service = CustomApplicationService(
        storage=PostgresStorage(session=Mock()), producer_service=Mock()
    )

    result = await application_service.get_applications(
        application_filters_without_username_dto_data
    )

    assert result == {
        "applications": applications_created_data_dict,
    }

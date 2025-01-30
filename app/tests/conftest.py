import asyncio
from datetime import datetime
from typing import Generator

import pytest
from app.domain.schemas import (ApplicationAddDTO, ApplicationDTO,
                                ApplicationFiltersDTO)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def application_add_data_dict() -> dict:
    return {
        "user_name": "test",
        "description": "test1",
    }


@pytest.fixture()
def application_add_data_dto(application_add_data_dict) -> ApplicationAddDTO:
    return ApplicationAddDTO(**application_add_data_dict)


@pytest.fixture
def applications_add_data_dict() -> list[dict]:
    return [
        {"user_name": "test", "description": "test1"},
        {"user_name": "test", "description": "test2"},
        {"user_name": "cat", "description": "meow"},
        {"user_name": "dog", "description": "woof"},
        {"user_name": "bird", "description": "tweet"},
    ]


@pytest.fixture()
def applications_add_data_dto(applications_add_data_dict) -> list[ApplicationAddDTO]:
    return [ApplicationAddDTO(**data) for data in applications_add_data_dict]


@pytest.fixture()
def applications_created_data_dict() -> list[dict]:
    return [
        {
            "id": 1,
            "user_name": "test",
            "description": "test1",
            "created_at": datetime.fromisoformat("2025-01-01T00:00:00"),
        },
        {
            "id": 2,
            "user_name": "test",
            "description": "test2",
            "created_at": datetime.fromisoformat("2025-01-02T00:00:00"),
        },
        {
            "id": 3,
            "user_name": "cat",
            "description": "meow",
            "created_at": datetime.fromisoformat("2025-01-03T00:00:00"),
        },
    ]


@pytest.fixture
def applications_created_data_dto(
    applications_created_data_dict,
) -> list[ApplicationDTO]:
    return [ApplicationDTO(**data) for data in applications_created_data_dict]


@pytest.fixture()
def application_filters_dto_data() -> ApplicationFiltersDTO:
    return ApplicationFiltersDTO(page=1, limit=5, user_name="test")


@pytest.fixture()
def application_filters_without_username_dto_data() -> ApplicationFiltersDTO:
    return ApplicationFiltersDTO(page=1, limit=5)

from typing import AsyncGenerator
from unittest.mock import patch

import pytest
import pytest_asyncio
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from app.config import settings
from app.config import settings as mocked_settings
from app.database import Base
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_docker_container():
    with PostgresContainer(image="postgres:16-alpine", driver="asyncpg").with_exposed_ports(
        settings.postgres_port
    ) as postgres_container:
        yield postgres_container


@pytest.fixture(scope="session")
def apply_migrations(postgres_docker_container):
    with patch("app.config.settings", mocked_settings):
        alembic_cfg = AlembicConfig("./app/alembic.ini")

        test_values = {
            'postgres_host': "127.0.0.1",
            'postgres_db': 'test',
            'postgres_user': 'test',
            'postgres_password': 'test',
            'postgres_port': postgres_docker_container.get_exposed_port(settings.postgres_port),
        }
        mocked_settings.__dict__.update(test_values)

        upgrade(alembic_cfg, "head")


@pytest_asyncio.fixture(scope="session")
async def engine(apply_migrations, postgres_docker_container) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(postgres_docker_container.get_connection_url())

    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, autocommit=False)


@pytest_asyncio.fixture(autouse=True)
async def clean_database(engine):
    async with (
        engine.connect() as connection,
        connection.begin() as transaction
    ):
        for table in reversed(Base.metadata.sorted_tables):
            await connection.execute(table.delete())

        await transaction.commit()


@pytest_asyncio.fixture()
async def session(session_maker: async_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
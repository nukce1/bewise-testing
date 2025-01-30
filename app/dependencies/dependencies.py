from typing import Annotated

from app.database import get_db_session
from app.protocols.applications import ApplicationService
from app.protocols.producer import ProducerService
from app.protocols.storage import Storage
from app.repository.postgres_repo import PostgresStorage
from app.services.application_service import CustomApplicationService
from app.services.producer_service import KafkaProducerService
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


def get_producer_service(request: Request) -> ProducerService:
    return KafkaProducerService(request.app.state.producer)


async def get_storage(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> Storage:
    return PostgresStorage(session)


def get_application_service(
    storage: Annotated[Storage, Depends(get_storage)],
    producer_service: Annotated[ProducerService, Depends(get_producer_service)],
) -> ApplicationService:
    return CustomApplicationService(storage, producer_service)

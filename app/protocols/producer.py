from typing import Protocol

from app.domain.schemas import ApplicationDTO


class ProducerService(Protocol):
    async def send_application_created(self, created_app: ApplicationDTO) -> None: ...

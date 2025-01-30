from typing import Protocol

from app.domain.schemas import ApplicationAddDTO, ApplicationFiltersDTO


class ApplicationService(Protocol):
    async def get_applications(
        self, application_filters: ApplicationFiltersDTO
    ) -> dict: ...

    async def create_application(self, application_data: ApplicationAddDTO) -> dict: ...

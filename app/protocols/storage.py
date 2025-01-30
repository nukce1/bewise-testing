from typing import Protocol

from app.domain.models import Application


class Storage(Protocol):
    async def get_applications_by_username_with_pagination(
        self, user_name: str, page: int, limit: int
    ) -> list[Application]: ...

    async def get_applications_with_pagination(
        self, page: int, limit: int
    ) -> list[Application]: ...

    async def create_application(
        self, user_name: str, description: str
    ) -> Application: ...

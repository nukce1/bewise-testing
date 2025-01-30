from datetime import datetime

from pydantic import BaseModel, Field


class ApplicationDTO(BaseModel):
    id: int
    user_name: str
    description: str
    created_at: datetime


class ApplicationAddDTO(BaseModel):
    user_name: str
    description: str


class ApplicationFiltersDTO(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=0, le=100)
    user_name: str | None = None

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_host: str = "db-host"
    postgres_port: int = 5432
    postgres_db: str = "bewise_db"
    postgres_user: str = "bewise"
    postgres_password: str = "bewise"

    producer_servers: list[str]
    topic_applications_created: str = "applications-created"

    log_level: str = "INFO"
    log_format: str
    log_date_format: str
    log_path: str

    @computed_field
    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

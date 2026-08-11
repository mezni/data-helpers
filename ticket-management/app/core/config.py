from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ticket Management API"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "ticket_management"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

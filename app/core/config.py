from __future__ import annotations
from enum import Enum
from functools import lru_cache
from typing import Literal, Any, Optional
from pydantic import AnyUrl, PostgresDsn, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class Env(str, Enum):
    development = "development"
    production = "production"

LogLevel = Literal["CRITICAL","ERROR","WARNING","INFO","DEBUG","NOTSET"]


class Settings(BaseSettings):
    ENV: Env = Env.development
    APP_NAME: str = "car-insurance"
    JOB_INTERVAL_MINUTES: int = 1
    LOG_LEVEL: Optional[LogLevel] = None

    CORS_ALLOW_ORIGINS: list[str] = ["*"]

    LOG_FILE_PATH: str = "logs/app.log"

    DATABASE_URL: Optional[str] = None
    DATABASE_URL_SYNC: Optional[str] = None

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env.development",               # util local; în producție folosește env vars / secrets
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def set_and_validate_db(cls, v: Optional[str], info: Any) -> str:
        env: Env = info.data.get("ENV", Env.development)
        if v:
            if env is Env.production:
                # verifică format Postgres; ridică eroare dacă nu e valid
                try:
                    PostgresDsn(v)
                except ValidationError as e:
                    raise ValueError(f"Invalid Postgres DSN for production: {e}") from e
            return v
        # fallback dev
        if env is Env.development:
            return "sqlite+aiosqlite:///./dev.db"
        raise ValueError("DATABASE_URL must be set for production")

    @field_validator("DATABASE_URL_SYNC", mode="before")
    @classmethod
    def set_and_validate_db_sync(cls, v: Optional[str], info: Any) -> str:
        env: Env = info.data.get("ENV", Env.development)
        if v:
            if env is Env.production:
                try:
                    PostgresDsn(v)
                except ValidationError as e:
                    raise ValueError(f"Invalid Postgres DSN for production: {e}") from e
            return v
        if env is Env.development:
            return "sqlite:///./dev.db"
        raise ValueError("DATABASE_URL_SYNC must be set for production")

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def default_log_level(cls, v, info):
        if v: return v
        return "DEBUG" if info.data.get("ENV", Env.development) is Env.development else "INFO"

@lru_cache
def get_settings() -> Settings:
    return Settings()

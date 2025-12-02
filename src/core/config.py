from typing import Literal
from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["development", "production"]

class DBSettings(BaseSettings):
    DB_HOST: str = Field(default="localhost", alias="DB_HOST")
    DB_PORT: int = Field(default=5432, alias="DB_PORT")
    DB_USER: str = Field(default="postgres", alias="DB_USER")
    DB_PASS: SecretStr = Field(..., alias="DB_PASS")
    DB_NAME: str = Field(..., alias="DB_NAME")
    DB_POOL_SIZE: int = Field(default=10, alias="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=5, alias="DB_MAX_OVERFLOW")

    def get_async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS.get_secret_value()}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    def get_sync_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS.get_secret_value()}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

class SecureSettings(BaseSettings):
    SECRET_KEY: SecretStr = Field(..., alias="SECRET_KEY")
    HASH_ALGORITHM: str = Field(default="HS256", alias="HASH_ALGORITHM")
    TOKEN_LIFETIME_DAYS: int = Field(default=7, alias="TOKEN_LIFETIME_DAYS")

    model_config = SettingsConfigDict(extra="ignore")

class Settings(BaseSettings):
    ENVIRONMENT: Environment = "development"
    DB: DBSettings = Field(default_factory=DBSettings)
    SECURE: SecureSettings = Field(default_factory=SecureSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
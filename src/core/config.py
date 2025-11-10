from typing import Literal
from functools import lru_cache

from pydantic_settings import BaseSettings

Environment = Literal["development", "production"]

class Settings(BaseSettings):
    ENVIRONMENT: Environment = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
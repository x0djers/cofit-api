from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)
from src.core.config import settings

engine = create_async_engine(
    settings.DB.get_async_url(),
    echo=settings.ENVIRONMENT == "development",
    future=True,
    pool_size=settings.DB.DB_POOL_SIZE,
    max_overflow=settings.DB.DB_MAX_OVERFLOW,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
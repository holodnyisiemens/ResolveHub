from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    settings.database_url_asyncpg,
    echo=False,
)

async_session_factory = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

sync_engine = create_engine(
    settings.database_url_syncpg,  # добавление синхронного URL в config
    echo=False,
    future=True
)
import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from app.core.config import settings
from app.core.database import Base
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.task_repository import TaskRepository


TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD.get_secret_value()}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/test_resolvehub"
)

@pytest.fixture()
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    try:
        yield engine
    finally:
        await engine.dispose()

@pytest.fixture()
async def tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def session(engine, tables):
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.fixture
async def employee_repository(session) -> EmployeeRepository:
    return EmployeeRepository(session)

@pytest.fixture
async def task_repository(session) -> TaskRepository:
    return TaskRepository(session)

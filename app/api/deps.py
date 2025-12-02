from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_factory
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.task_repository import TaskRepository
from app.services.employee_service import EmployeeService
from app.services.task_service import TaskService


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии базы данных"""
    async with async_session_factory() as session:
        yield session

async def provide_employee_repository(
    db_session: AsyncSession = Depends(provide_db_session),
) -> EmployeeRepository:
    """Провайдер репозитория сотрудников"""
    return EmployeeRepository(db_session)

async def provide_employee_service(
    employee_repository: EmployeeRepository = Depends(provide_employee_repository),
) -> EmployeeService:
    """Провайдер сервиса сотрудников"""
    return EmployeeService(employee_repository)

async def provide_task_repository(
    db_session: AsyncSession = Depends(provide_db_session),
) -> TaskRepository:
    """Провайдер репозитория задач"""
    return TaskRepository(db_session)

async def provide_task_service(
    task_repository: TaskRepository = Depends(provide_task_repository),
    employee_repository: EmployeeRepository = Depends(provide_employee_repository),
) -> TaskService:
    """Провайдер сервиса задач"""
    return TaskService(task_repository, employee_repository)

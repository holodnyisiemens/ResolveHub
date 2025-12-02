from fastapi import APIRouter, Depends
from typing import List
from app.schemas.task import TaskDTO
from app.repositories.task_repository import TaskRepository
from app.core.database import async_session
from app.auth import get_current_employee

router = APIRouter()

@router.get("/tasks/me", response_model=List[TaskDTO])
async def get_my_tasks(current_employee = Depends(get_current_employee)):
    async with async_session() as session:
        repo = TaskRepository(session)
        tasks = await repo.list_by_assignee(current_employee.id)
        return tasks

@router.post("/tasks/{task_id}/assign", response_model=TaskDTO)
async def assign_task(task_id: int, current_employee = Depends(get_current_employee)):
    async with async_session() as session:
        repo = TaskRepository(session)
        task = await repo.assign_task(task_id, current_employee.id)
        return task

@router.post("/tasks/{task_id}/close", response_model=TaskDTO)
async def close_task(task_id: int, current_employee = Depends(get_current_employee)):
    async with async_session() as session:
        repo = TaskRepository(session)
        task = await repo.close_task(task_id, current_employee.id)
        return task
from fastapi import APIRouter, Depends

from app.api.deps import provide_task_service
from app.schemas.task import TaskAddDTO, TaskDTO, TaskUpdateDTO
from app.services.task_service import TaskService


router = APIRouter(tags=["Tasks"])


@router.get("/", response_model=list[TaskDTO])
async def get_all_tasks(
    task_service: TaskService = Depends(provide_task_service),
):
    """Получить все задачи"""
    return await task_service.get_all()

@router.get("/{task_id:int}", response_model=TaskDTO)
async def get_task_by_id(
    task_id: int,
    task_service: TaskService = Depends(provide_task_service),
):
    """Получить задачу по id"""
    return await task_service.get_by_id(task_id)

@router.post("/", response_model=TaskDTO)
async def create_task(
    task_data: TaskAddDTO,
    task_service: TaskService = Depends(provide_task_service),
):
    """Создать задачу"""
    return await task_service.create(task_data)

@router.delete("/{task_id:int}")
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(provide_task_service),
):
    """Удалить задачу"""
    await task_service.delete(task_id)

@router.put("/{task_id:int}", response_model=TaskDTO)
async def update_task(
    task_id: int,
    task_data: TaskUpdateDTO,
    task_service: TaskService = Depends(provide_task_service),
):
    """Обновить данные задачи"""
    return await task_service.update(task_id, task_data)

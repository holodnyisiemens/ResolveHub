from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskAddDTO, TaskUpdateDTO


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        return await self.session.get(Task, task_id)

    async def create(self, task_data: TaskAddDTO) -> Task:
        task = Task(**task_data.model_dump())
        self.session.add(task)
        
        await self.session.flush()
        await self.session.refresh(task)
        
        return task

    async def delete(self, task: Task) -> None:
        await self.session.delete(task)
        await self.session.flush()

    async def update(self, task: Task, task_data: TaskUpdateDTO) -> Task:
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await self.session.flush()
        await self.session.refresh(task)

        return task

    async def get_all(self) -> list[Task]:
        stmt = select(Task)
        result = await self.session.execute(stmt)
        return result.scalars().all()
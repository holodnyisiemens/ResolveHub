from datetime import date, datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskStatus
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
    
    async def get_assigned(self) -> list[Task]:
        """Задачи с назначенным сотрудником"""
        stmt = select(Task).where(Task.assignee_id.is_not(None))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_unassigned(self) -> list[Task]:
        """Задачи без назначенного сотрудника"""
        stmt = select(Task).where(Task.assignee_id.is_(None))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_filtered_tasks(
        self,
        status_filter: Optional[TaskStatus] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> list[Task]:
        """
        Фильтрация задач по статусу и периоду создания
        
        Args:
            status_filter: Фильтр по статусу (None = все)
            start_date: Дата начала периода (None = без ограничения)
            end_date: Дата окончания периода (None = без ограничения)
        """
        stmt = select(Task)
        
        filters = []

        if status_filter is not None:
            filters.append(Task.status == status_filter)

        if start_date is not None:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            filters.append(Task.created_at >= start_datetime)

        if end_date is not None:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            filters.append(Task.created_at <= end_datetime)
        
        if filters:
            stmt = stmt.where(*filters)

        stmt = stmt.order_by(Task.created_at.desc())

        result = await self.session.execute(stmt)
        return result.scalars().all()

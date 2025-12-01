import pytest

from app.models.task import Task
from app.schemas.task import TaskAddDTO, TaskUpdateDTO
from app.repositories.task_repository import TaskRepository


task_data_1 = TaskAddDTO(
    title="Fix backend bug",
    description="Error 500",
    creator_email="alexey@example.com",
)

task_data_2 = TaskAddDTO(
    title="Fix frontend bug",
    description="Loading 1 min",
    creator_email="alexander@example.com",
)


class TestTaskRepository:
    async def _create_test_task(self, task_repository: TaskRepository, task_data: TaskAddDTO) -> Task:
        return await task_repository.create(task_data)

    @pytest.mark.asyncio
    async def test_create_task(self, task_repository: TaskRepository):
        task = await self._create_test_task(task_repository, task_data_1)

        assert task.id is not None
        assert task.title == task_data_1.title
        assert task.description == task_data_1.description
        assert task.creator_email == task_data_1.creator_email

    @pytest.mark.asyncio
    async def test_update_task(self, task_repository: TaskRepository):
        task = await self._create_test_task(task_repository, task_data_1)

        new_task_data = TaskUpdateDTO(title="Resolved")

        await task_repository.update(task, new_task_data)
        updated_task = await task_repository.get_by_id(task.id)

        assert updated_task.title == new_task_data.title

        assert updated_task.id == task.id
        assert updated_task.description == task.description
        assert updated_task.creator_email == task.creator_email

    @pytest.mark.asyncio
    async def test_delete_task(self, task_repository: TaskRepository):
        task = await self._create_test_task(task_repository, task_data_1)
        await task_repository.delete(task)

        found_task = await task_repository.get_by_id(task.id)
        assert found_task is None

    @pytest.mark.asyncio
    async def test_get_all(self, task_repository: TaskRepository):
        await self._create_test_task(task_repository, task_data_1)
        await self._create_test_task(task_repository, task_data_2)

        tasks_list = await task_repository.get_all()

        task_creator_emails = [task.creator_email for task in tasks_list]

        assert len(tasks_list) == 2
        assert task_creator_emails[0] == task_data_1.creator_email
        assert task_creator_emails[1] == task_data_2.creator_email

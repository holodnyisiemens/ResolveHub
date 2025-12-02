from fastapi import HTTPException

from app.repositories.employee_repository import EmployeeRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskAddDTO, TaskDTO, TaskUpdateDTO


class TaskService:
    def __init__(self, task_repo: TaskRepository, employee_repo: EmployeeRepository):
        self.task_repo = task_repo
        self.employee_repo = employee_repo

    async def get_by_id(self, task_id: int) -> TaskDTO:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        
        return TaskDTO.model_validate(task)

    async def create(self, task_data: TaskAddDTO) -> TaskDTO:
        try:
            task = await self.task_repo.create(task_data)
            await self.task_repo.session.commit()
        except:
            await self.task_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Task creation error")

        return TaskDTO.model_validate(task)

    async def delete(self, task_id: int) -> None:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

        try:
            await self.task_repo.delete(task)
            await self.task_repo.session.commit()
        except:
            await self.task_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Task delete error")

    async def update(self, task_id: int, task_data: TaskUpdateDTO) -> TaskDTO:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

        if task_data.assignee_id is not None:
            assignee = await self.employee_repo.get_by_id(task_data.assignee_id)
            if not assignee:
                raise HTTPException(status_code=404, detail=f"Employee with ID {task_data.assignee_id} does not exist")

        try:
            await self.task_repo.update(task, task_data)
            await self.task_repo.session.commit()
        except:
            await self.task_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Task update error")    

        return TaskDTO.model_validate(task)

    async def get_all(self) -> list[TaskDTO]:
        task_list = await self.task_repo.get_all()
        return [TaskDTO.model_validate(task) for task in task_list]

from fastapi import HTTPException

from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeAddDTO, EmployeeDTO, EmployeeUpdateDTO


class EmployeeService:
    def __init__(self, employee_repo: EmployeeRepository):
        self.employee_repo = employee_repo

    async def get_by_id(self, employee_id: int) -> EmployeeDTO:
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")
        
        return EmployeeDTO.model_validate(employee)

    async def create(self, employee_data: EmployeeAddDTO) -> EmployeeDTO:
        if await self.employee_repo.get_by_email(employee_data.email):
            raise HTTPException(status_code=409, detail=f"Employee with email {employee_data.email} already exists")

        try:
            employee = await self.employee_repo.create(employee_data)
            await self.employee_repo.session.commit()
        except:
            await self.employee_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Employee creation error")

        return EmployeeDTO.model_validate(employee)

    async def delete(self, employee_id: int) -> None:
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

        try:
            await self.employee_repo.delete(employee)
            await self.employee_repo.session.commit()
        except:
            await self.employee_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Employee delete error")   

    async def update(self, employee_id: int, employee_data: EmployeeUpdateDTO) -> EmployeeDTO:
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

        if employee_data.email is not None:
            existing_employee = await self.employee_repo.get_by_email(employee_data.email)
            if existing_employee and existing_employee.id != employee.id:
                raise HTTPException(
                    status_code=409,
                    detail=f"Email {employee_data.email} is already used by another employee",
            )

        try:
            await self.employee_repo.update(employee, employee_data)
            await self.employee_repo.session.commit()
        except:
            await self.employee_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Employee update error")    

        return EmployeeDTO.model_validate(employee)

    async def get_by_username(self, username: str) -> EmployeeDTO:
        employee = await self.employee_repo.get_by_username(username)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee with username {username} not found")
        
        return EmployeeDTO.model_validate(employee)

    async def get_by_email(self, email: str) -> EmployeeDTO:
        employee = await self.employee_repo.get_by_email(email)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee with email {email} not found")
        
        return EmployeeDTO.model_validate(employee)

    async def get_all(self) -> list[EmployeeDTO]:
        employee_list = await self.employee_repo.get_all()
        return [EmployeeDTO.model_validate(employee) for employee in employee_list]
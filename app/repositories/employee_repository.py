from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.schemas.employee import EmployeeAddDTO, EmployeeUpdateDTO


class EmployeeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, employee_id: int) -> Optional[Employee]:
        return await self.session.get(Employee, employee_id)

    async def create(self, employee_data: EmployeeAddDTO) -> Employee:
        employee = Employee(**employee_data.model_dump())
        self.session.add(employee)
        
        await self.session.flush()
        await self.session.refresh(employee)
        
        return employee

    async def delete(self, employee_id: int) -> bool:
        employee = await self.session.get(Employee, employee_id)
        if not employee:
            return False
        
        await self.session.delete(employee)
        await self.session.flush()
        return True

    async def update(self, employee_id: int, employee_data: EmployeeUpdateDTO) -> Optional[Employee]:
        employee = await self.session.get(Employee, employee_id)
        if not employee:
            return None

        update_data = employee_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(employee, field, value)

        await self.session.flush()
        await self.session.refresh(employee)

        return employee

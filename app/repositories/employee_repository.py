from typing import Optional

from sqlalchemy import select
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

    async def delete(self, employee: Employee) -> None:
        await self.session.delete(employee)
        await self.session.flush()

    async def update(self, employee: Employee, employee_data: EmployeeUpdateDTO) -> Employee:
        update_data = employee_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(employee, field, value)

        await self.session.flush()
        await self.session.refresh(employee)

        return employee

    async def get_by_username(self, employee_username: str) -> Optional[Employee]:
        stmt = select(Employee).where(Employee.username == employee_username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, employee_email: str) -> Optional[Employee]:
        stmt = select(Employee).where(Employee.email == employee_email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Employee]:
        stmt = select(Employee)
        result = await self.session.execute(stmt)
        return result.scalars().all()
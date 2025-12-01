import pytest

from app.models.employee import Employee
from app.schemas.employee import EmployeeAddDTO, EmployeeUpdateDTO
from app.repositories.employee_repository import EmployeeRepository


employee_data_1 = EmployeeAddDTO(
    username="alexey",
    email="alexey@example.com",
)

employee_data_2 = EmployeeAddDTO(
    username="alexander",
    email="alexander@example.com",
)


class TestEmployeeRepository:
    async def _create_test_employee(self, employee_repository: EmployeeRepository, employee_data: EmployeeAddDTO) -> Employee:
        return await employee_repository.create(employee_data)

    @pytest.mark.asyncio
    async def test_create_employee(self, employee_repository: EmployeeRepository):
        employee = await self._create_test_employee(employee_repository, employee_data_1)

        assert employee.id is not None
        assert employee.username == employee_data_1.username
        assert employee.email == employee_data_1.email

    @pytest.mark.asyncio
    async def test_update_employee(self, employee_repository: EmployeeRepository):
        employee = await self._create_test_employee(employee_repository, employee_data_1)

        new_employee_data = EmployeeUpdateDTO(username="Updated")

        await employee_repository.update(employee.id, new_employee_data)
        updated_employee = await employee_repository.get_by_id(employee.id)

        assert updated_employee.username == new_employee_data.username

        assert updated_employee.id == employee.id
        assert updated_employee.email == employee.email

    @pytest.mark.asyncio
    async def test_delete_employee(self, employee_repository: EmployeeRepository):
        employee = await self._create_test_employee(employee_repository, employee_data_1)
        await employee_repository.delete(employee.id)

        found_employee = await employee_repository.get_by_id(employee.id)
        assert found_employee is None

from fastapi import APIRouter, Depends

from app.api.deps import provide_employee_service
from app.schemas.employee import EmployeeAddDTO, EmployeeDTO, EmployeeUpdateDTO
from app.services.employee_service import EmployeeService


router = APIRouter(tags=["Employees"])


@router.get("/", response_model=list[EmployeeDTO])
async def get_all_employees(
    employee_service: EmployeeService = Depends(provide_employee_service),
):
    """Получить всех сотрудников"""
    return await employee_service.get_all()


@router.get("/{employee_id:int}", response_model=EmployeeDTO)
async def get_employee_by_id(
    employee_id: int,
    employee_service: EmployeeService = Depends(provide_employee_service), 
):
    """Получить сотрудника по id"""
    return await employee_service.get_by_id(employee_id)


@router.post("/", response_model=EmployeeDTO)
async def create_employee(
    employee_data: EmployeeAddDTO,
    employee_service: EmployeeService = Depends(provide_employee_service),
):
    """Создать сотрудника"""
    return await employee_service.create(employee_data)


@router.delete("/{employee_id:int}")
async def delete_employee(
    employee_id: int,
    employee_service: EmployeeService = Depends(provide_employee_service),
):
    """Удалить сотрудника"""
    await employee_service.delete(employee_id)


@router.put("/{employee_id:int}", response_model=EmployeeDTO)
async def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdateDTO,
    employee_service: EmployeeService = Depends(provide_employee_service),
):
    """Обновить данные сотрудника"""
    return await employee_service.update(employee_id, employee_data)

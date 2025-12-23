from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.di.deps import provide_task_service, provide_employee_service
from app.models.task import TaskStatus
from app.services.task_service import TaskService
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/tasks")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def tasks_page(
    request: Request,
    status: Optional[str] = Query(None, description="Статус задачи"),
    start_date: Optional[str] = Query(None, description="Дата начала (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Дата окончания (YYYY-MM-DD)"),
    task_service: TaskService = Depends(provide_task_service)
):
    # Конвертируем статус в Enum, если указан
    task_status = TaskStatus(status) if status else None

    # Конвертируем даты, если они не пустые строки
    start_dt = date.fromisoformat(start_date) if start_date else None
    end_dt = date.fromisoformat(end_date) if end_date else None

    tasks = await task_service.get_filtered_tasks(
        status_filter=task_status,
        start_date=start_dt,
        end_date=end_dt,
    )

    context = {
        "request": request,
        "tasks": tasks,
        "filters": {
            "status": status or "",
            "start_date": start_date or "",
            "end_date": end_date or "",
        },
        "status_options": list(TaskStatus)
    }
    return templates.TemplateResponse("tasks.html", context)

@router.get("/{task_id}/", response_class=HTMLResponse)
async def task_detail_page(
    request: Request,
    task_id: int,
    task_service: TaskService = Depends(provide_task_service),
    employee_service: EmployeeService = Depends(provide_employee_service),
):
    
    task = await task_service.get_by_id(task_id)
    if task is None:
        return HTMLResponse(status_code=404, content="Task not found")

    employees = await employee_service.get_all_employees()

    context = {
        "request": request,
        "task": task,
        "employees": employees,
    }
    return templates.TemplateResponse("task_detail.html", context)

@router.post("/{task_id}/", response_class=HTMLResponse)
async def assign_task_page(
    request: Request,
    task_id: int,
    assignee_id: Optional[int] = Form(None),
    task_service: TaskService = Depends(provide_task_service),
):
    await task_service.assign_task(task_id=task_id, assignee_id=assignee_id)
    # допускаем None = снять исполнителя
    await task_service.assign_task(task_id=task_id, assignee_id=assignee_id)

    # редирект обратно на страницу задачи
    return RedirectResponse(
        url=f"/tasks/{task_id}/",
        status_code=303,
    )

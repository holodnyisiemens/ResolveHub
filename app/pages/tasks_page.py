from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.di.deps import provide_employee_service, provide_task_service
from app.email_worker.sender import send_autoreply_task_done
from app.models.task import TaskStatus
from app.schemas.task import TaskUpdateDTO
from app.services.employee_service import EmployeeService
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks")
templates = Jinja2Templates(directory="app/templates/html")


@router.get("/", response_class=HTMLResponse)
async def tasks_page(
    request: Request,
    status: Optional[str] = Query(None, description="Статус задачи"),
    start_date: Optional[str] = Query(None, description="Дата начала (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Дата окончания (YYYY-MM-DD)"),
    task_service: TaskService = Depends(provide_task_service),
    employee_service: EmployeeService = Depends(provide_employee_service),
):
    task_status = TaskStatus(status) if status else None

    start_dt = date.fromisoformat(start_date) if start_date else None
    end_dt = date.fromisoformat(end_date) if end_date else None

    tasks = await task_service.get_filtered_tasks(
        status_filter=task_status,
        start_date=start_dt,
        end_date=end_dt,
    )

    employees = await employee_service.get_all()

    context = {
        "request": request,
        "tasks": tasks,
        "employees": employees,
        "filters": {
            "status": status or "",
            "start_date": start_date or "",
            "end_date": end_date or "",
        },
        "status_options": list(TaskStatus),
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

    employees = await employee_service.get_all()
    status_options = list(TaskStatus)

    context = {
        "request": request,
        "task": task,
        "employees": employees,
        "status_options": status_options,
    }
    return templates.TemplateResponse("task_detail.html", context)


@router.post("/{task_id}/")
async def update_task_page(
    request: Request,
    task_id: int,
    status: str = Form(...),
    assignee_id: str = Form(None),
    task_service: TaskService = Depends(provide_task_service),
):
    # Если исполнитель остается/становится неназначеным преобразуем пустую строку в None
    if assignee_id == "":
        assignee_id = None
    else:
        try:
            assignee_id = int(assignee_id)
        except Exception as e:
            print(e)

    update_data = TaskUpdateDTO(
        status=TaskStatus(status),
        assignee_id=assignee_id,
    )
    updated_task = await task_service.update(task_id=task_id, task_data=update_data)

    if updated_task.status == TaskStatus.DONE:
        print(f"Task from {updated_task.creator_email} was closed")
        send_autoreply_task_done(
            to_email=updated_task.creator_email,
            subject=updated_task.title,
            body=updated_task.description,
        )

    return RedirectResponse(
        url=f"/tasks/{task_id}/",
        status_code=303,
    )

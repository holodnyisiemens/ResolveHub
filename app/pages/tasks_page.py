from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.di.deps import provide_task_service
from app.models.task import TaskStatus
from app.services.task_service import TaskService

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

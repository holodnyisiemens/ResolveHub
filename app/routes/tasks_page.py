from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_factory
from app.repositories.task_repository import TaskRepository
from app.models.task import TaskStatus
from datetime import date
from typing import Optional

router = APIRouter(prefix="/tasks", tags=["tasks"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def tasks_page(
    request: Request,
    status: Optional[str] = Query(None, description="Статус задачи"),
    start_date: Optional[str] = Query(None, description="Дата начала (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Дата окончания (YYYY-MM-DD)")
):
    # Ручная валидация: все поля обязательны для показа задач
    if not status or not start_date or not end_date:
        return templates.TemplateResponse(
            "tasks.html",
            {
                "request": request,
                "assigned_tasks": [],
                "unassigned_tasks": [],
                "filters": {"status": status, "start_date": start_date, "end_date": end_date},
                "error_message": "Заполните все поля фильтров для просмотра задач"
            }
        )
    
    try:
        # Конвертируем строки в нужные типы
        task_status = TaskStatus(status)
        start_dt = date.fromisoformat(start_date)
        end_dt = date.fromisoformat(end_date)
        
        # Проверяем логику дат
        if start_dt > end_dt:
            return templates.TemplateResponse(
                "tasks.html",
                {
                    "request": request,
                    "assigned_tasks": [],
                    "unassigned_tasks": [],
                    "filters": {"status": status, "start_date": start_date, "end_date": end_date},
                    "error_message": "Дата начала не может быть позже даты окончания"
                }
            )
        
        async with async_session_factory() as session:
            repo = TaskRepository(session)
            
            all_tasks = await repo.get_filtered_tasks(task_status, start_dt, end_dt)
            
            assigned_tasks = [t for t in all_tasks if t.assignee_id is not None]
            unassigned_tasks = [t for t in all_tasks if t.assignee_id is None]
            
            if not all_tasks:
                return templates.TemplateResponse(
                    "tasks.html",
                    {
                        "request": request,
                        "assigned_tasks": [],
                        "unassigned_tasks": [],
                        "filters": {"status": status, "start_date": start_date, "end_date": end_date},
                        "error_message": "Таких заданий нет"
                    }
                )
            
            return templates.TemplateResponse(
                "tasks.html",
                {
                    "request": request,
                    "assigned_tasks": assigned_tasks,
                    "unassigned_tasks": unassigned_tasks,
                    "filters": {"status": status, "start_date": start_date, "end_date": end_date}
                }
            )
            
    except ValueError as e:
        return templates.TemplateResponse(
            "tasks.html",
            {
                "request": request,
                "assigned_tasks": [],
                "unassigned_tasks": [],
                "filters": {"status": status, "start_date": start_date, "end_date": end_date},
                "error_message": f"Неверный формат данных: {str(e)}"
            }
        )

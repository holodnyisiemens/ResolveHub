from fastapi import APIRouter

from app.api.v1.employee import router as employee_router
from app.api.v1.task import router as task_router
from app.core.config import settings

router = APIRouter()

router.include_router(
    employee_router,
    prefix=settings.api.v1.employees,
)

router.include_router(
    task_router,
    prefix=settings.api.v1.tasks,
)
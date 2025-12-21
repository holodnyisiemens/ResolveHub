from fastapi import FastAPI
from sqladmin import Admin

from app.core.database import async_engine
from app.auth import AdminAuth
from app.admin.admin import EmployeeAdmin, TaskAdmin
from starlette.middleware.sessions import SessionMiddleware

from app.api import router as api_router
from app.core.config import settings

from app.routes.tasks_page import router as tasks_page_router

app = FastAPI(title="ResolveHub")
app.include_router(
    api_router,
    prefix=settings.api.prefix,
)

# Middleware для сессий и для работы AdminAuth
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Подключаем админку
admin = Admin(
    app,
    async_engine,
    authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY)
)

# Регистрируем представления моделей в админке
admin.add_view(EmployeeAdmin)
admin.add_view(TaskAdmin)

app.include_router(tasks_page_router, include_in_schema=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="app.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )

from fastapi import FastAPI
from sqladmin import Admin

from app.core.database import sync_engine
from app.auth import AdminAuth
from app.admin.admin import EmployeeAdmin, TaskAdmin
from starlette.middleware.sessions import SessionMiddleware

from app.api import router as api_router
from app.core.config import settings

app = FastAPI()
app.include_router(
    api_router,
    prefix=settings.api.prefix,
)
# Middleware для сессий и для работы AdminAuth
app.add_middleware(SessionMiddleware, secret_key="SUPER_SECRET_KEY")

# Подключаем админку
admin = Admin(
    app,
    sync_engine,
    authentication_backend=AdminAuth(secret_key="SUPER_SECRET_KEY")
)

# Регистрируем представления моделей в админке
admin.add_view(EmployeeAdmin)
admin.add_view(TaskAdmin)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="app.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
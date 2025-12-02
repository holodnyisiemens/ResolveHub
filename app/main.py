from fastapi import FastAPI
from sqladmin import Admin

from app.core.database import sync_engine
from app.auth import AdminAuth
from app.admin.admin import EmployeeAdmin, TaskAdmin
from app.routes.employee_router import router as employee_router
from app.routes.task_router import router as task_router
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Подключаем API роутеры
app.include_router(employee_router, prefix="/employees", tags=["employees"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])  # Роутинг для tasks

# Добавьте middleware для сессий — обязательно для работы AdminAuth
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
    uvicorn.run("main:app", reload=True)
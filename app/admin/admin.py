from sqladmin import ModelView

from app.core.security import get_password_hash
from app.models.employee import Employee
from app.models.task import Task


class EmployeeAdmin(ModelView, model=Employee):
    column_list = [
        Employee.id,
        Employee.username,
        Employee.email,
        Employee.is_active,
        Employee.is_superuser,
    ]

    form_columns = [
        Employee.username,
        Employee.email,
        Employee.hashed_password,
        Employee.is_active,
        Employee.is_superuser,
    ]

    column_labels = {
        Employee.hashed_password: "Password",
    }

    async def create_model(self, request, data):
        plain_password = data.get("hashed_password")
        if not plain_password:
            raise ValueError("Password is required for new employee")
        data["hashed_password"] = get_password_hash(plain_password)
        return await super().create_model(request, data)

    async def update_model(self, request, pk, data):
        plain_password = data.get("hashed_password")
        if plain_password:
            data["hashed_password"] = get_password_hash(plain_password)
        else:
            data.pop("hashed_password", None)
        return await super().update_model(request, pk, data)


class TaskAdmin(ModelView, model=Task):
    form_columns = [
        Task.title,
        Task.description,
        Task.creator_email,
        Task.status,
        Task.assignee,
        Task.created_at,
    ]

    column_list = [
        Task.id,
        Task.title,
        Task.description,
        Task.creator_email,
        Task.status,
        Task.assignee,
        Task.created_at,
    ]

from typing import Any

from fastapi import Request
from sqladmin import ModelView
from wtforms import PasswordField

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

    # Переопределяем виджет для скрытия пароля
    form_overrides = {
        "hashed_password": PasswordField,
    }

    column_labels = {
        Employee.hashed_password: "Password",
    }

    async def on_model_change(
        self,
        data: dict[str, Any],
        model: Employee,
        is_created: bool,
        request: Request,
    ) -> None:
        password = data.get("hashed_password")

        # Пароль обязателен при создании
        if is_created and not password:
            raise ValueError("Password is required")

        # Если пароль введён — хэшируем
        if password:
            data["hashed_password"] = get_password_hash(password)

        await super().on_model_change(data, model, is_created, request)


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

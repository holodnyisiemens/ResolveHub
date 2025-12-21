from sqladmin import ModelView
from app.models.employee import Employee
from app.models.task import Task


class EmployeeAdmin(ModelView, model=Employee):
    form_columns = [
        Employee.username,
        Employee.email,
        Employee.hashed_password,
        Employee.is_active,
        Employee.is_superuser,
    ]

    column_list = [
        Employee.id,
        Employee.username,
        Employee.email,
        Employee.is_active,
        Employee.is_superuser,
    ]


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

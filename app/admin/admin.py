from fastapi import FastAPI
from sqladmin import Admin, ModelView
from app.core.database import sync_engine
from app.models.employee import Employee
from app.models.task import Task

app = FastAPI()

admin = Admin(app, engine=sync_engine, title="Admin Panel")

class EmployeeAdmin(ModelView, model=Employee):
    column_list = [Employee.id, Employee.username, Employee.email, Employee.is_active]

class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.title, Task.description, Task.creator_email, Task.status, Task.assignee_id]

admin.add_view(EmployeeAdmin)
admin.add_view(TaskAdmin)
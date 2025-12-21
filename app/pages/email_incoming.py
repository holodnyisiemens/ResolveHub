from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from app.schemas.task import TaskAddDTO
from app.repositories.task_repository import TaskRepository
from app.core.database import async_session_factory

class IncomingEmail(BaseModel):
    subject: str
    body: str
    from_email: EmailStr

router = APIRouter()

@router.post("/email-incoming")
async def receive_email(email: IncomingEmail):
    async with async_session_factory() as session:
        repo = TaskRepository(session)
        task = await repo.create(TaskAddDTO(
            title=email.subject,
            description=email.body,
            creator_email=email.from_email
        ))
        return {"message": "Task created", "task_id": task.id}
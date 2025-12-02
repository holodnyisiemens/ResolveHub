from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_tasks():
    return {"message": "List of tasks"}
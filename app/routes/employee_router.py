from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_employees():
    return {"message": "List of employees"}
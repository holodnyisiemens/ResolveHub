import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi import FastAPI
import uvicorn
from app.admin.admin import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.admin.admin:app", host="127.0.0.1", port=8000, reload=True)

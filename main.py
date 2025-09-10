from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.head("/")
def read_root(): ...


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

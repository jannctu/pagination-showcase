from fastapi import FastAPI
from .routers import router as api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API"}

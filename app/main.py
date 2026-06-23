from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} API"}

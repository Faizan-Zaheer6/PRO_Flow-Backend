from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import global_exception_handler
from app.core.rate_limit import RateLimiter
from app.api.api import api_router

# Setup logging
setup_logging()

app = FastAPI(title=settings.APP_NAME)

# Add custom exception handler
app.add_exception_handler(Exception, global_exception_handler)

# Include all API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} API"}

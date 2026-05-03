from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import SessionDep
from app.services.auth import auth_service
from app.schemas.token import Token

from app.core.rate_limit import RateLimiter

router = APIRouter()

@router.post("/login", response_model=Token, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def login_access_token(
    session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    return await auth_service.authenticate_user(session, form_data)

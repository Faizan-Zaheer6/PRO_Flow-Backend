from fastapi import APIRouter, Depends
from typing import Annotated
from app.api.deps import SessionDep, get_current_admin_user, get_current_active_user
from app.services.user import user_service
from app.schemas.user import User, UserCreate
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(
    *,
    session: SessionDep,
    user_in: UserCreate,
):
    return await user_service.create_user(session, user_in)

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)]
):
    return current_user

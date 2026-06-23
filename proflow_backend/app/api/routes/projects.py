from fastapi import APIRouter, Depends
from typing import Annotated
from app.api.deps import SessionDep, get_current_active_user
from app.services.project import project_service
from app.schemas.project import Project, ProjectCreate
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/", response_model=Project)
async def create_project(
    *,
    session: SessionDep,
    project_in: ProjectCreate,
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return await project_service.create_project(session, project_in, current_user)

@router.get("/", response_model=list[Project])
async def read_projects(
    session: SessionDep,
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
):
    return await project_service.get_projects(session, skip=skip, limit=limit)

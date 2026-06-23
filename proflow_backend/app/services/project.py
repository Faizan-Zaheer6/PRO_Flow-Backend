from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.project import project_repo
from app.schemas.project import ProjectCreate
from app.models.user import User

class ProjectService:
    async def create_project(self, session: AsyncSession, project_in: ProjectCreate, current_user: User):
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Only admins can create projects")
            
        project_dict = project_in.model_dump()
        project_dict["owner_id"] = current_user.id
        return await project_repo.create(session, obj_in=project_dict)

    async def get_projects(self, session: AsyncSession, skip: int, limit: int):
        return await project_repo.get_multi(session, skip=skip, limit=limit)

project_service = ProjectService()

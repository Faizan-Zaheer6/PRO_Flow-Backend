from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.project import Project

class ProjectRepository(BaseRepository[Project]):
    async def get_by_owner(self, session: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100):
        result = await session.execute(
            select(Project)
            .filter(Project.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

project_repo = ProjectRepository(Project)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.repositories.base import BaseRepository
from app.models.task import Task

class TaskRepository(BaseRepository[Task]):
    async def get_by_assignee(self, session: AsyncSession, assignee_id: int, skip: int = 0, limit: int = 100):
        result = await session.execute(
            select(Task)
            .filter(Task.assignee_id == assignee_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_project(self, session: AsyncSession, project_id: int, skip: int = 0, limit: int = 100):
        result = await session.execute(
            select(Task)
            .filter(Task.project_id == project_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_tasks_by_status(self, session: AsyncSession, status: str) -> int:
        result = await session.execute(
            select(func.count(Task.id)).filter(Task.status == status)
        )
        return result.scalar_one()

task_repo = TaskRepository(Task)

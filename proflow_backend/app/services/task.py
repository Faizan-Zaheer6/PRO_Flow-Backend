from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.task import task_repo
from app.schemas.task import TaskCreate
from app.models.user import User
from app.core.redis import redis_client

class TaskService:
    async def create_task(self, session: AsyncSession, task_in: TaskCreate, current_user: User):
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Only admins can create tasks")
            
        task_dict = task_in.model_dump()
        task = await task_repo.create(session, obj_in=task_dict)
        
        await redis_client.delete("dashboard:stats")
        
        return task

    async def get_tasks(self, session: AsyncSession, skip: int, limit: int, current_user: User):
        if current_user.role == "admin":
            return await task_repo.get_multi(session, skip=skip, limit=limit)
        else:
            return await task_repo.get_by_assignee(session, assignee_id=current_user.id, skip=skip, limit=limit)

task_service = TaskService()

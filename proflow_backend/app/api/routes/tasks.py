from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Annotated
from app.api.deps import SessionDep, get_current_active_user
from app.services.task import task_service
from app.schemas.task import Task, TaskCreate
from app.models.user import User as UserModel

router = APIRouter()

def send_mock_email(email: str, title: str):
    import time
    time.sleep(2)  # Simulate network delay
    print(f"Mock Email sent to {email} for Task: {title}")

@router.post("/", response_model=Task)
async def create_task(
    *,
    session: SessionDep,
    task_in: TaskCreate,
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    background_tasks: BackgroundTasks
):
    task = await task_service.create_task(session, task_in, current_user)
    
    if task.assignee_id:
        background_tasks.add_task(send_mock_email, "assignee@example.com", task.title)
        
    return task

@router.get("/", response_model=list[Task])
async def read_tasks(
    session: SessionDep,
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
):
    return await task_service.get_tasks(session, skip=skip, limit=limit, current_user=current_user)

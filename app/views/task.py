from fastapi import APIRouter
from app.schemas.task import Task, TaskStatusUpdate
from app.crud import task_crud

task_views = APIRouter()


@task_views.post("/update", response_model=Task)
async def update(task_status_update: TaskStatusUpdate):
    task = await task_crud.update_status_by_id(task_status_update)

    return task

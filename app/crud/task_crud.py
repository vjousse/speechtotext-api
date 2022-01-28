import logging
from typing import Optional
from pydantic import UUID4

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskStatusUpdate
from app.core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


async def create(task_create: TaskCreate, media_file_id: int) -> Task:

    new_task = await Task.create(
        **task_create.dict(), media_file_id=media_file_id
    )

    return new_task


async def get(id: UUID4) -> Optional[Task]:
    task = await Task.get_or_none(id=id)
    return task


async def update_status_by_id(task_status_update: TaskStatusUpdate) -> Task:

    logger.debug(f"#### Trying to get task with id {task_status_update.id}")
    task = await get(task_status_update.id)

    task.status = task_status_update.status
    await task.save()
    return task

from pydantic import BaseModel, UUID4
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    ENQUEUED = "enqueued"
    DELAYED = "delayed"
    RUNNING = "running"
    FAILED = "failed"
    DONE = "done"
    SKIPPED = "skipped"


class TaskBase(BaseModel):
    id: UUID4
    status: str
    message_data: bytes
    actor_name: str
    queue_name: str
    asr_model_id: int


class TaskStatusUpdate(BaseModel):
    id: UUID4
    status: TaskStatus


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    media_file_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True

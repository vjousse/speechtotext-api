from pydantic import BaseModel, UUID4
from datetime import datetime


class ResultBase(BaseModel):
    filename: str


class ResultCreate(ResultBase):
    message_id: UUID4
    pass


class Result(ResultBase):
    id: int
    media_file_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True

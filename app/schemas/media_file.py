from typing import List
from pydantic import BaseModel, UUID4
from datetime import datetime
from app.models.media_file import MediaFile as MediaFileModel
from tortoise.contrib.pydantic import pydantic_model_creator


class MediaFileBase(BaseModel):
    filename: str
    duration: int = 0
    size: int = 0


class MediaFileCreate(MediaFileBase):
    pass


class MediaFile(MediaFileBase):
    id: int
    user_id: UUID4
    updated_at: datetime
    created_at: datetime
    uuid: UUID4

    class Config:
        orm_mode = True


MediaFilePopulated = pydantic_model_creator(
    MediaFileModel, name="MediaFilePopulated"
)


class FilesList(BaseModel):
    total_count: int
    offset: int
    limit: int
    files: List[MediaFilePopulated]

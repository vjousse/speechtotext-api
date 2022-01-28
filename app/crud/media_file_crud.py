from typing import List
from fastapi import UploadFile
from pathlib import Path
import uuid

from app.models.media_file import MediaFile
from app.schemas.media_file import MediaFileCreate
from app.models.user import UserModel
from app.core.config import settings
from app.services import file_service


async def create(
    media_file_create: MediaFileCreate, user_id: uuid.UUID
) -> MediaFile:

    new_media_file = await MediaFile.create(
        **media_file_create.dict(), uuid=uuid.uuid4(), user_id=user_id
    )

    return new_media_file


async def move_to_upload(media_file: MediaFile, file: UploadFile) -> bool:

    file_service.save_upload_file(
        file, Path(settings.UPLOAD_DIR, media_file.uploaded_filename())
    )

    return True


async def count_all_for_user(user: UserModel) -> int:

    count = await MediaFile.filter(user_id=user.id).all().count()

    return count


async def get_all_for_user(
    user: UserModel, offset: int = 0, limit: int = 10
) -> List[MediaFile]:

    files = (
        await MediaFile.filter(user_id=user.id)
        .order_by("-created_at")
        .limit(limit)
        .offset(offset)
        .all()
        .prefetch_related("tasks", "results", "tasks__asr_model")
    )

    return files

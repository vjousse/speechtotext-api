import logging
from typing import Optional
from fastapi import UploadFile
from pathlib import Path

from app.models.result import Result
from app.schemas.result import ResultCreate
from app.core.config import settings
from app.services import file_service
from app.crud import task_crud

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


async def create(
        result_create: ResultCreate) -> Result:

    task = await task_crud.get(id=result_create.message_id)

    media_file_id = None

    if task:
        media_file_id = task.media_file_id


    new_result = await Result.create(
        **result_create.dict(),
        media_file_id = media_file_id)

    return new_result


async def get(id: int) -> Optional[Result]:
    result = await Result.get_or_none(id=id)
    return result


async def move_to_upload(
        result: ResultCreate,
        file: UploadFile) -> bool:

    file_service.save_upload_file(
        file,
        Path(settings.UPLOAD_DIR, result.filename)
    )

    return True

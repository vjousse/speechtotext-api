import logging
from typing import List
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException

from app.core.config import settings
from app.models.user import UserModel
from app.schemas.media_file import\
    MediaFile, MediaFileCreate, FilesList
from app.crud import media_file_crud, asr_model_crud
from app.services.fastapi_users import fastapi_users

from asr_worker.download import download_url

file_views = APIRouter()

current_active_user = fastapi_users.current_user(active=True)

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


@file_views.post(
    "/upload/",
    response_model=List[MediaFile],
    status_code=201)
async def create_upload_file(asr_model_id: int = Form(...),
                             files: List[UploadFile] = File(...),
                             user: UserModel = Depends(current_active_user)):

    media_files: List[MediaFile] = []

    for file in files:
        create_object = MediaFileCreate(
            filename=file.filename,
            duration=0,
            size=0,
            owned_id=user.id)

        media_file = await media_file_crud.create(create_object, user.id)

        asr_model = await asr_model_crud.get(asr_model_id)

        if not asr_model:
            raise HTTPException(
                status_code=404,
                detail=f"Asr model with id {asr_model_id} not found")

        download_url.send_with_options(
            args=(
                f"{settings.UPLOAD_URL}/"
                f"{media_file.uploaded_filename()}",
                asr_model.label
            ),
            media_file_id=media_file.id,
            asr_model_id=asr_model_id
        )

        await media_file_crud.move_to_upload(media_file, file)

        media_files.append(media_file)

    return media_files


@file_views.get(
    "/",
    response_model=FilesList)
async def list_files(offset: int = 0, limit: int = 10,
                     user: UserModel = Depends(current_active_user)):

    files = await media_file_crud.get_all_for_user(user, offset, limit)

    files_list = FilesList(
        total_count=await media_file_crud.count_all_for_user(user),
        offset=offset,
        limit=limit,
        files=files)

    return files_list

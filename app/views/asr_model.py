import logging
from fastapi import APIRouter, Depends
from typing import List

from app.core.config import settings
from app.services.fastapi_users import fastapi_users
from app.schemas.asr_model import AsrModel
from app.models.user import UserModel
from app.crud import asr_model_crud

asr_model_views = APIRouter()

current_active_user = fastapi_users.current_user(active=True)

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


@asr_model_views.get("/", response_model=List[AsrModel])
async def list_models(user: UserModel = Depends(current_active_user)):

    models = await asr_model_crud.get_all()

    return models

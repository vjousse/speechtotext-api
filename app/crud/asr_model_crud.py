import logging
from typing import List, Optional

from app.models.asr_model import AsrModel
from app.schemas.asr_model import AsrModelCreate
from app.core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


async def create(asr_model_create: AsrModelCreate) -> AsrModel:

    new_asr_model = await AsrModel.create(**asr_model_create.dict())

    return new_asr_model


async def get(id: int) -> Optional[AsrModel]:
    result = await AsrModel.get_or_none(id=id)
    return result


async def get_all() -> List[AsrModel]:

    models = await AsrModel.all().order_by("lang")

    return models

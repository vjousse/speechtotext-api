from typing import List

from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel
from app.models import user
from app.schemas import media_file


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB, PydanticModel):
    items: List[media_file.MediaFile] = []

    class Config:
        orm_mode = True
        orig_model = user.UserModel

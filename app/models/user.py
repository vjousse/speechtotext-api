from fastapi_users.db import TortoiseBaseUserModel
from tortoise import fields


class UserModel(TortoiseBaseUserModel):

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

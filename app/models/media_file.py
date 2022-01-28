from tortoise.models import Model
from tortoise import fields
from app.models.task import Task
from app.models.result import Result

import os


class MediaFile(Model):
    id = fields.IntField(pk=True)
    filename = fields.CharField(max_length=255)
    duration = fields.IntField()
    size = fields.IntField()
    user = fields.ForeignKeyField(
        'models.UserModel',
        related_name='media_files')

    tasks: fields.ReverseRelation["Task"]
    results: fields.ReverseRelation["Result"]

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    uuid = fields.UUIDField()

    def __str__(self):
        return self.filename

    def uploaded_filename(self):
        _, file_extension = os.path.splitext(self.filename)
        return f"{self.uuid}{file_extension}"

    class PydanticMeta:
        # Let's exclude the created timestamp
        exclude = ("user",)

from tortoise.models import Model
from tortoise import fields
from app.schemas.asr_model import Lang


class AsrModel(Model):
    id = fields.IntField(pk=True)
    label = fields.CharField(max_length=255, unique=True)
    description = fields.TextField()

    lang = fields.CharField(
        max_length=30,
        choices=[(enum.value, enum.value.capitalize()) for enum in Lang],
        default=Lang.EN.value,
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.label

from tortoise.models import Model
from tortoise import fields


class Result(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(pk=True)
    filename = fields.CharField(max_length=255)
    media_file = fields.ForeignKeyField(
        "models.MediaFile", related_name="results"
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter
    def __str__(self):
        return self.filename

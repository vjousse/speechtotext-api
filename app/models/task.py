from tortoise.models import Model
from tortoise import fields
from dramatiq import Message
from app.schemas.task import TaskStatus


class Task(Model):

    id = fields.UUIDField(pk=True)

    status = fields.CharField(
        max_length=8,
        choices=[(enum.value, enum.value.capitalize()) for enum in TaskStatus],
        default=TaskStatus.ENQUEUED.value)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True, db_index=True)
    message_data = fields.BinaryField()

    actor_name = fields.CharField(max_length=300, null=True)
    queue_name = fields.CharField(max_length=100, null=True)

    media_file = fields.ForeignKeyField(
        'models.MediaFile',
        related_name='tasks')

    asr_model = fields.ForeignKeyField(
        'models.AsrModel',
        related_name='tasks')

    def message(self):
        return Message.decode(bytes(self.message_data))

    def __str__(self):
        return str(self.message)

import asyncio
import logging
import dramatiq

from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend
from dramatiq.results import Results
from dramatiq.middleware import Middleware
from dramatiq.middleware import CurrentMessage

from app.core.config import settings
from app.crud import task_crud

from app.schemas.task import TaskCreate, TaskStatus

import requests

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


class StatusMiddleware(Middleware):
    """This middleware keeps track of task executions.
    """

    def log(self, message, status, actor_name, queue_name, media_file_id):

        print(f"Msg: {message} - Status: {status} - "
              f"Actor name: {actor_name} - Queue name: {queue_name} - "
              f"MediaFile Id: {media_file_id}")

    def after_enqueue(self, broker, message, delay):

        logger.debug("Creating Task from message %r.", message.message_id)

        status = TaskStatus.ENQUEUED.value
        if delay:
            status = TaskStatus.DELAYED.value

        media_file_id = message.options.get("media_file_id")
        asr_model_id = message.options.get("asr_model_id")

        task_create = TaskCreate(
            id=message.message_id,
            status=status,
            message_data=0,
            actor_name=message.actor_name,
            queue_name=message.queue_name,
            asr_model_id=asr_model_id)

        asyncio.create_task(
            task_crud.create(task_create, media_file_id))

        self.log(
            message,
            status=status,
            actor_name=message.actor_name,
            queue_name=message.queue_name,
            media_file_id=media_file_id,
        )

    def before_process_message(self, broker, message):

        logger.debug("Updating Task from message %r.", message.message_id)
        media_file_id = message.options.get("media_file_id")

        status = TaskStatus.RUNNING.value

        # Update the status
        requests.post(f"{settings.BASE_URL}/api/tasks/update",
                      json={"id": message.message_id, "status": status})
        self.log(
            message,
            status=status,
            actor_name=message.actor_name,
            queue_name=message.queue_name,
            media_file_id=media_file_id,
        )

    def after_skip_message(self, broker, message):

        self.after_process_message(
            broker, message, status=TaskStatus.SKIPPED.value)

    def after_process_message(self, broker, message, *, result=None,
                              exception=None, status=None):

        if exception is not None:
            status = TaskStatus.FAILED.value
        elif status is None:
            status = TaskStatus.DONE.value

        logger.debug("Updating Task from message %r.", message.message_id)
        logger.debug(f"Result {result}")

        media_file_id = message.options.get("media_file_id")

        # Update the status
        requests.post(f"{settings.BASE_URL}/api/tasks/update",
                      json={"id": message.message_id, "status": status})

        self.log(
            message,
            status=status,
            actor_name=message.actor_name,
            queue_name=message.queue_name,
            media_file_id=media_file_id,
        )


def init_dramatiq():
    backend = RedisBackend(
        host=settings.REDIS_HOST, password=settings.REDIS_PASSWORD)

    broker = RedisBroker(
        host=settings.REDIS_HOST, password=settings.REDIS_PASSWORD)
    broker.add_middleware(Results(backend=backend))
    broker.add_middleware(StatusMiddleware())
    broker.add_middleware(CurrentMessage())

    dramatiq.set_broker(broker)
    broker = dramatiq.get_broker()

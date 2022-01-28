import logging
import os
from app.core.config import settings

# Init tortoise model before hand, otherwise pydantic model
# creation will not include relations

from tortoise import Tortoise

Tortoise.init_models(settings.TORTOISE_MODELS, "models")


from app.core.init import create_app  # noqa: E402

# Mute Tortoise Logger
logger = logging.getLogger("tortoise")
logger.setLevel(logging.INFO)

# Mute Multipart logger
logger = logging.getLogger("multipart.multipart")
logger.setLevel(logging.INFO)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))


app = create_app()

from pydantic import BaseSettings
import os

current_dir = os.path.dirname(os.path.realpath(__file__))


def get_db_uri(user, passwd, host, db):
    return f"postgres://{user}:{passwd}@{host}:5432/{db}"


class Settings(BaseSettings):
    ALLOWED_MIMETYPES = [
        "audio/aac",
        "audio/flac",
        "audio/ogg",
        "audio/mpeg",
        "audio/mp4",
        "audio/wav",
    ]

    APP_NAME: str = "SpeechToText API"
    APP_VERSION: str = "0.0.1"

    BASE_URL: str = "http://localhost:8000"

    CORS_ALLOWED_ORIGINS = [
        "*"
    ]

    LOG_LEVEL = "DEBUG"

    DB_URL: str = "postgres://postgres:@localhost:5432/speechtotext_api_dev"

    REDIS_HOST: str = "localhost"
    REDIS_PASSWORD: str = ""

    SECRET: str = "MyAwesomeSecr€t"

    TORTOISE_MODELS = [
        "app.models.asr_model",
        "app.models.media_file",
        "app.models.result",
        "app.models.task",
        "app.models.user",
        "aerich.models",  # Aerich migrations tool
    ]

    # Uploads should be served by a static web server
    UPLOAD_DIR = os.path.join(current_dir, "..", "..", "uploads")
    UPLOAD_URL = "/uploads"

    # Assets should be served by a static web server
    ASSETS_DIR = os.path.join(current_dir, "..", "..", "assets")
    ASSETS_URL = "/assets"

    WORKER_DOCKER_COMMAND = \
        "/opt/asr/kaldi/system/simply_decode.pl"

    WORKER_OUTPUT_DIRECTORY = \
        "/opt/asr/kaldi/output"


settings = Settings()

# Used by aerich
TORTOISE_ORM = {
    "connections": {
        "default": settings.DB_URL
    },
    "apps": {
        "models": {
            "models": settings.TORTOISE_MODELS,
            "default_connection": "default",
        },
    },
}

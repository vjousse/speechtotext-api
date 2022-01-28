import os
import asyncio
import pytest
import glob
from tortoise.contrib.test import finalizer, initializer
from typing import Generator
from fastapi.testclient import TestClient
from fastapi_users.password import get_password_hash

from app.core.config import settings
from app.core.init import create_app
from app.models.user import UserModel
from app.models.asr_model import AsrModel
from app.schemas.asr_model import AsrModelCreate
from app.schemas.asr_model import Lang
from app.crud import asr_model_crud

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope="session")
def app() -> Generator:
    settings.DB_URL = "sqlite://:memory:"
    settings.UPLOAD_DIR = os.path.join(dir_path, "uploads")
    app = create_app()
    yield app

    files = glob.glob(f"{settings.UPLOAD_DIR}/*")
    for f in files:
        os.remove(f)


@pytest.fixture(scope="module")
def client(app) -> Generator:
    db_url = os.environ.get("TORTOISE_TEST_DB", settings.DB_URL)

    initializer(settings.TORTOISE_MODELS, db_url=db_url, app_label="models")

    with TestClient(app) as c:
        yield c

    finalizer()


@pytest.fixture(scope="module")
def myclient() -> Generator:
    settings.DB_URL = "sqlite://:memory:"
    app = create_app()
    db_url = os.environ.get("TORTOISE_TEST_DB", settings.DB_URL)

    initializer(settings.TORTOISE_MODELS, db_url=db_url, app_label="models")

    with TestClient(app) as c:
        yield c

    finalizer()


@pytest.fixture(scope="module")
def my_event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


excalibur_password_hash = get_password_hash("excalibur")


@pytest.fixture(scope="module")
def default_model(event_loop: asyncio.AbstractEventLoop) -> AsrModel:

    asr_model_create = AsrModelCreate(
        label="fr.kaldi", description="French Kaldi model", lang=Lang.FR
    )

    asr_model = event_loop.run_until_complete(
        asr_model_crud.create(asr_model_create)
    )

    return asr_model


@pytest.fixture(scope="module")
def verified_user() -> UserModel:
    return UserModel(
        email="lake.lady@camelot.bt",
        hashed_password=excalibur_password_hash,
        is_active=True,
        is_verified=True,
    )


@pytest.fixture(scope="module")
def db_verified_user(
    verified_user, event_loop: asyncio.AbstractEventLoop
) -> UserModel:

    event_loop.run_until_complete(verified_user.save())

    return verified_user

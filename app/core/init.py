from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from fastapi_users import FastAPIUsers

from app.core.config import settings
from app.services.fastapi_users import fastapi_users, auth_backend

from app.services.dramatiq import init_dramatiq


def create_app() -> FastAPI:

    init_dramatiq()

    app = FastAPI(
        docs_url="/docs", title=settings.APP_NAME, version=settings.APP_VERSION
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.views.file import file_views
    from app.views.info import info_views
    from app.views.auth import auth_views
    from app.views.task import task_views
    from app.views.result import result_views
    from app.views.asr_model import asr_model_views

    app.include_router(file_views, prefix="/files", tags=["Files"])
    app.include_router(info_views, prefix="/infos", tags=["Info"])
    app.include_router(task_views, prefix="/tasks", tags=["Task"])
    app.include_router(result_views, prefix="/results", tags=["Result"])
    app.include_router(
        asr_model_views, prefix="/asr_models", tags=["Asr Models"]
    )
    app.include_router(auth_views, tags=["Custom auth"])

    app.mount(
        settings.UPLOAD_URL,
        StaticFiles(directory=settings.UPLOAD_DIR),
        name="uploads",
    )

    app.mount(
        settings.ASSETS_URL,
        StaticFiles(directory=settings.ASSETS_DIR),
        name="assets",
    )

    register_fastapi_users(app)

    register_tortoise(
        app,
        db_url=settings.DB_URL,
        modules={"models": settings.TORTOISE_MODELS},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    return app


def register_fastapi_users(app: FastAPI) -> FastAPIUsers:

    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
    )

    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(),
        prefix="/auth",
        tags=["auth"],
    )

    return fastapi_users

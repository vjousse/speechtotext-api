from fastapi import APIRouter
from app.core.config import settings

info_views = APIRouter()


@info_views.get("")
async def info():
    return {"allowed_mimetypes": settings.ALLOWED_MIMETYPES}

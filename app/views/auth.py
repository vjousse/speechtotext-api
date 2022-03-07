from fastapi import APIRouter, Depends, Response

from app.services.fastapi_users import fastapi_users, bearer_transport

auth_views = APIRouter()

current_active_user = fastapi_users.current_user(active=True)


@auth_views.post("/auth/jwt/refresh")
async def refresh_jwt(
    response: Response, user=Depends(fastapi_users.current_user(active=True))
):
    return await bearer_transport.get_login_response(user, response)

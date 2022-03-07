from fastapi import APIRouter, Depends, Response

from app.services.fastapi_users import (
    bearer_transport,
    fastapi_users,
    get_jwt_strategy,
)

auth_views = APIRouter()

current_active_user = fastapi_users.current_user(active=True)


@auth_views.post("/auth/jwt/refresh")
async def refresh_jwt(
    response: Response, user=Depends(fastapi_users.current_user(active=True))
):

    strategy = get_jwt_strategy()
    token = await strategy.write_token(user)
    return await bearer_transport.get_login_response(token, response)

from fastapi_users import FastAPIUsers
from app.schemas.user import User, UserCreate, UserDB, UserUpdate
from app.models.user import UserModel
from fastapi_users.db import TortoiseUserDatabase
from fastapi_users.authentication import JWTAuthentication,\
    CookieAuthentication

from app.core.config import settings

auth_backends = []

cookie_authentication = CookieAuthentication(
    secret=settings.SECRET,
    lifetime_seconds=3600*24)

auth_backends.append(cookie_authentication)

jwt_authentication = JWTAuthentication(
    secret=settings.SECRET,
    lifetime_seconds=3600,
    tokenUrl="/auth/jwt/login"
)

auth_backends.append(jwt_authentication)

user_db = TortoiseUserDatabase(UserDB, UserModel)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

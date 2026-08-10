from fastapi import APIRouter

from api.api_v1.fastapi_users import fastapi_users
from api.dependencies.authentication.backend import authentication_backend

router = APIRouter(
    prefix="/api/api_v1/auth",
    tags=["auth"],
)

router.include_router(
    router = fastapi_users.get_auth_router(authentication_backend),
)
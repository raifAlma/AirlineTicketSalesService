from fastapi import APIRouter

from api.api_v1.fastapi_users import fastapi_users
from api.dependencies.authentication.backend import authentication_backend
from api.schemas.user import UserRead, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(authentication_backend,
                                  requires_verification = True )
)
# /register
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

#/forgot-password
#/reset-password

router.include_router(
    fastapi_users.get_reset_password_router(),
)
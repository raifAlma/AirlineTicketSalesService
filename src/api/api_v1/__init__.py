from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from .auth import router as auth_router
from .user import router as user_router
from .messages import router as messages_router
from .airport import router as airport_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(messages_router)
router.include_router(airport_router)

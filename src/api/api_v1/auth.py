from fastapi import APIRouter

router = APIRouter(
    prefix="/api/api_v1/auth",
    tags=["auth"],
)
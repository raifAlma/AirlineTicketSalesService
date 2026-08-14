from fastapi import APIRouter
from fastapi import Depends, HTTPException

from api.api_v1.fastapi_users import current_active_user, current_active_superuser
from api.schemas.user import UserRead
from infrastructure.database.postgresql.models import User

router = APIRouter(
    prefix="/messeges",
    tags=["Messeges"],
)

@router.get('')
def get_user_messages(
        user: User = Depends(current_active_user),
):
    return {"message": "Hello User",
            'user': UserRead.model_validate(user)}


@router.get('/secrets')
def get_superuser_messages(
        user: User = Depends(current_active_superuser),
):
    return {"message": "Hello SuperUser",
            'user': UserRead.model_validate(user)}
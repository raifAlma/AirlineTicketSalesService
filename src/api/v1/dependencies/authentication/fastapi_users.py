import uuid

from api.v1.dependencies.user_manager import get_user_manager
from fastapi_users import FastAPIUsers
from .backend import authentication_backend
from infrastructure.database.postgresql.models import User
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [authentication_backend],
)
import asyncio
import contextlib

from api.dependencies.authentication.users import get_user_db
from api.dependencies.authentication.user_manager import get_user_manager
from api.shemas.user import UserCreate
from infrastructure.authentication.user_manager import UserManager
from infrastructure.database.postgresql.models import User
from infrastructure.database.postgresql.session import get_async_session
from fastapi_users.exceptions import UserAlreadyExists

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser(
    email: str,
    password: str,
    full_name: str = "",
    phone: str = "",
    is_active: bool = True,
    is_superuser: bool = True,
    is_verified: bool = True,
    role: str = "admin"
) -> User:
    user_create = UserCreate(
        email=email,
        password=password,
        full_name=full_name,
        phone=phone,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
        role=role,
    )

    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await create_user(
                        user_manager=user_manager,
                        user_create=user_create,
                    )
                    print(f"User created: {user}")
                    return user
    except UserAlreadyExists:
        print(f"User {email} already exists")
        raise



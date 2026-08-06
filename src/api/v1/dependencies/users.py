from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.database.postgresql.models import User
from infrastructure.database.postgresql.session import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield User.get_db(session=session)



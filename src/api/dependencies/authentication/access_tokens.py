from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.database.postgresql.models import AccessToken
from infrastructure.database.postgresql.session import get_async_session


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield AccessToken.get_db(session=session)
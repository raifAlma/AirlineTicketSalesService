from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.postgres.airline.airline import (
    PostgreSQLAirlineRepository,
)


class PostgreSQLAirlineUnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

        self.repository: PostgreSQLAirlineRepository | None = None

    async def __aenter__(self):
        self.repository = PostgreSQLAirlineRepository(self._session)
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

        await self._session.close()
        self.repository = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

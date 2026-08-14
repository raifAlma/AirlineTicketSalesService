from sqlalchemy.ext.asyncio.session import AsyncSession

from container import Container
from infrastructure.repositories.postgres.airport import PostgreSQLAirportUnitOfWork


def build_airport_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLAirportUnitOfWork:
    return Container.airport_uow_factory(session=session)
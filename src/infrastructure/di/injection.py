from sqlalchemy.ext.asyncio.session import AsyncSession

from container import Container
from infrastructure.repositories.postgres.aircraft import PostgreSQLAircraftUnitOfWork
from infrastructure.repositories.postgres.airport import PostgreSQLAirportUnitOfWork


def build_airport_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLAirportUnitOfWork:
    return Container.airport_uow_factory(session=session)

def build_aicraft_unit_of_work_factory(
    session: AsyncSession,
) -> PostgreSQLAircraftUnitOfWork:
    return Container.aicraft_uow_factory(session=session)
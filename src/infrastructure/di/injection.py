from sqlalchemy.ext.asyncio.session import AsyncSession

from container import Container
from infrastructure.repositories.postgres.aircraft import PostgreSQLAircraftUnitOfWork
from infrastructure.repositories.postgres.airline.uow import PostgreSQLAirlineUnitOfWork
from infrastructure.repositories.postgres.airport import PostgreSQLAirportUnitOfWork


def build_airport_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLAirportUnitOfWork:
    return Container.airport_uow_factory(session=session)


def build_aircraft_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLAircraftUnitOfWork:
    return Container.aircraft_uow_factory(session=session)


def build_airline_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLAirlineUnitOfWork:
    return Container.airline_uow_factory(session=session)

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_airport_unit_of_work
from infrastructure.repositories.postgres.airport import PostgreSQLAirportUnitOfWork
from usecases.airport.create_airport.implementation import (
    PostgreSQLCreateAirportUseCase,
)
from usecases.airport.get_airport.implementation import PostgreSQLGetAirportUseCase


def get_airport_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLAirportUnitOfWork:
    return build_airport_unit_of_work(session)


def create_airport_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_airport_unit_of_work(session)
    return PostgreSQLCreateAirportUseCase(uow=uow)


def get_by_id_airport_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_airport_unit_of_work(session)
    return PostgreSQLGetAirportUseCase(uow=uow)

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_airport_unit_of_work
from infrastructure.repositories.postgres.airport import PostgreSQLAirportUnitOfWork
from usecases.airport.create.implementation import (
    PostgreSQLCreateAirportUseCase,
)
from usecases.airport.delete.implementation import PostgreSQLDeleteAirportUseCase
from usecases.airport.get.implementation import PostgreSQLGetAirportUseCase
from usecases.airport.search.implementation import PostgreSQLSearchAirportUseCase


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


def search_airport_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_airport_unit_of_work(session)
    return PostgreSQLSearchAirportUseCase(uow=uow)


def delete_airport_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_airport_unit_of_work(session)
    return PostgreSQLDeleteAirportUseCase(uow=uow)

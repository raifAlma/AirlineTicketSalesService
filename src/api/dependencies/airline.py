from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_airline_unit_of_work
from infrastructure.repositories.postgres.airline.uow import PostgreSQLAirlineUnitOfWork
from usecases.airline.create.implementation import PostgreSQLCreateAirlineUseCase


def get_airline_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLAirlineUnitOfWork:
    return build_airline_unit_of_work(session)


def create_airline_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_airline_unit_of_work(session)
    return PostgreSQLCreateAirlineUseCase(uow=uow)

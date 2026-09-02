from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import  build_aircraft_unit_of_work
from infrastructure.repositories.postgres.aircraft import PostgreSQLAircraftUnitOfWork
from usecases.aircraft.create.implementation import PostgreSQLCreateAircraftUseCase
from usecases.aircraft.delete.implementation import PostgreSQLDeleteAircraftUseCase
from usecases.aircraft.get.implementation import PostgreSQLGetAircraftUseCase
from usecases.aircraft.search.implementation import PostgreSQLSearchAircraftUseCase


def get_aircraft_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLAircraftUnitOfWork:
    return build_aircraft_unit_of_work(session)

def create_aircraft_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_aircraft_unit_of_work(session)
    return PostgreSQLCreateAircraftUseCase(uow=uow)


def get_aircraft_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_aircraft_unit_of_work(session)
    return PostgreSQLGetAircraftUseCase(uow=uow)

def search_aircraft_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_aircraft_unit_of_work(session)
    return PostgreSQLSearchAircraftUseCase(uow=uow)

def delete_aircraft_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_aircraft_unit_of_work(session)
    return PostgreSQLDeleteAircraftUseCase(uow=uow)
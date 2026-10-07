from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from api.api_v1.fastapi_users import current_active_superuser
from api.dependencies.aircraft import create_aircraft_use_case
from api.dependencies.airline import (
    create_airline_use_case,
    delete_airline_use_case,
    get_by_id_airline_use_case,
    search_airline_use_case,
    update_airline_use_case,
)
from api.schemas.aircraft import CreateAircraftSchema, ResponseAircraftSchema
from api.schemas.airline import CreateAirlineSchema, ResponseCreateAirlineSchema, UpdateAirlineSchema
from domain.validators.aircraft.aircraft_exceptions import InvalidAircraftField
from domain.validators.airline.airline_exception import InvalidAirlineField
from infrastructure.database.postgresql.models import User
from infrastructure.repositories.postgres.aircraft.exception import (
    AircraftAlreadyExists,
)
from infrastructure.repositories.postgres.airline.exception import (
    AirlineAlreadyExists,
    AirlineNotFound,
)
from infrastructure.types import AircraftIdType, AirlineIdType
from usecases.aircraft.create.abstract import AbstractCreateAircraftUseCase
from usecases.airline.create.abstract import AbstractCreateAirlineUseCase
from usecases.airline.delete.abstract import AbstractDeleteAirlineUseCase
from usecases.airline.get_by_id.abstract import AbstractGetByIdAirlineUseCase
from usecases.airline.search.abstract import AbstractSearchAirlineUseCase
from usecases.airline.update.abstract import AbstractAirlineUpdateUseCase

router = APIRouter(
    prefix="/airline",
    tags=["Airline"],
)


@router.post("", response_model=ResponseCreateAirlineSchema, status_code=201)
async def create_airline(
    payload: CreateAirlineSchema,
    usecase: AbstractCreateAirlineUseCase = Depends(create_airline_use_case),
    _: User = Depends(current_active_superuser),
):
    try:
        airline = await usecase.execute(payload)
    except InvalidAirlineField as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AirlineAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    return airline


@router.get("/search", response_model=List[ResponseAircraftSchema], status_code=200)
async def search_airline(
    q: str = Query(..., min_length=1, max_length=100),
    usecase: AbstractSearchAirlineUseCase = Depends(search_airline_use_case),
):
    return await usecase.execute(q)


@router.post(
    "/{airline_id}/aircraft", response_model=ResponseAircraftSchema, status_code=201
)
async def create_aircraft(
    airline_id: AircraftIdType,
    payload: CreateAircraftSchema,
    usecase: AbstractCreateAircraftUseCase = Depends(create_aircraft_use_case),
    _: User = Depends(current_active_superuser),
):
    try:
        aircraft = await usecase.execute(airline_id, payload)
    except InvalidAircraftField as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AircraftAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    return aircraft


@router.get("/{id}", response_model=ResponseCreateAirlineSchema, status_code=200)
async def get_by_id(
    id: AirlineIdType,
    usecase: AbstractGetByIdAirlineUseCase = Depends(get_by_id_airline_use_case),
    _: User = Depends(current_active_superuser),
):
    try:
        airline = await usecase.execute(id)
    except AirlineNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return airline


@router.put("/{id}", response_model=ResponseCreateAirlineSchema, status_code=200)
async def update(
        id: AirlineIdType,
        payload: UpdateAirlineSchema,
        usecase: AbstractAirlineUpdateUseCase = Depends(update_airline_use_case),
        _: User = Depends(current_active_superuser),
):
    try:
        airline = await usecase.execute(id, payload)
    except AirlineNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidAirlineField as e:
        raise HTTPException(status_code=422, detail=str(e))
    return airline

@router.delete("/{id}", status_code=204)
async def delete(
    id: AirlineIdType,
    usecase: AbstractDeleteAirlineUseCase = Depends(delete_airline_use_case),
    _: User = Depends(current_active_superuser),
):
    try:
        await usecase.execute(id)
    except AirlineNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None

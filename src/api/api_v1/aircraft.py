from fastapi import APIRouter, Depends, HTTPException, Query

from api.api_v1.fastapi_users import current_active_superuser
from api.dependencies.aircraft import (
    create_aircraft_use_case,
    delete_aircraft_use_case,
    get_aircraft_use_case,
    search_aircraft_use_case,
    update_aircraft_use_case,
)
from api.schemas.aircraft import (
    CreateAircraftSchema,
    ResponseAircraftSchema,
    UpdateAircraftSchema,
)
from domain.validators.aircraft.aircraft_exceptions import InvalidAircraftField
from infrastructure.database.postgresql.models import User
from infrastructure.repositories.postgres.aircraft.exception import (
    AircraftNotFound,
)
from infrastructure.types import AircraftIdType
from usecases.aircraft.get.abstract import AbstractGetAircraftUseCase
from usecases.aircraft.search.abstract import AbstractSearchAircraftUseCase
from usecases.aircraft.update.abstract import AbstractAircraftUpdateUseCase
from usecases.airport.delete.abstract import AbstractDeleteAirportUseCase


router = APIRouter(
    prefix="/aircraft",
    tags=["Aircraft"],
)




@router.get("/search", response_model=list[ResponseAircraftSchema], status_code=200)
async def search_aircraft(
    q: str = Query(..., min_length=1, max_length=100),
    usecase: AbstractSearchAircraftUseCase = Depends(search_aircraft_use_case),
):
    return await usecase.execute(q)


@router.get("/{id}", response_model=ResponseAircraftSchema, status_code=200)
async def get_aircraft(
    payload: AircraftIdType,
    usecase: AbstractGetAircraftUseCase = Depends(get_aircraft_use_case),
):
    try:
        aircraft = await usecase.execute(payload)
    except AircraftNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return aircraft


@router.delete("/{id}", status_code=204)
async def delete_aircraft(
    id: AircraftIdType,
    _: User = Depends(current_active_superuser),
    usecase: AbstractDeleteAirportUseCase = Depends(delete_aircraft_use_case),
):
    try:
        await usecase.execute(id)
    except AircraftNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None


@router.put("/{id}", response_model=ResponseAircraftSchema, status_code=200)
async def update_aircraft(
    id: AircraftIdType,
    payload: UpdateAircraftSchema,
    _: User = Depends(current_active_superuser),
    usecase: AbstractAircraftUpdateUseCase = Depends(update_aircraft_use_case),
):
    try:
        aircraft = await usecase.execute(id, payload)
    except AircraftNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return aircraft

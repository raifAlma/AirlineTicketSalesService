from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from api.api_v1.fastapi_users import current_active_superuser
from api.dependencies.aircraft import create_aircraft_use_case, get_aircraft_use_case
from api.schemas.aircraft import ResponseAircraftSchema, CreateAircraftSchema
from infrastructure.database.postgresql.models import User
from infrastructure.repositories.postgres.aircraft.exception import AircraftAlreadyExists, AircraftNotFound
from infrastructure.types import AircraftIdType
from usecases.aircraft.create.abstract import AbstractCreateAircraftUseCase
from usecases.aircraft.get.abstract import AbstractGetAircraftUseCase

router = APIRouter(
    prefix="/aircraft",
    tags=["Aircraft"],
)

@router.post("", response_model=ResponseAircraftSchema, status_code=201)
async def create_aircraft(
        payload: CreateAircraftSchema,
        usecase: AbstractCreateAircraftUseCase = Depends(create_aircraft_use_case),
        _: User = Depends(current_active_superuser),
):
    try:
        aircraft = await usecase.execute(payload)
    except AircraftAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    return aircraft

@router.get("", response_model=ResponseAircraftSchema, status_code=200)
async def get_aircraft(
        payload: AircraftIdType,
        usecase: AbstractGetAircraftUseCase = Depends(get_aircraft_use_case)
):
    try:
        aircraft = await usecase.execute(payload)
    except AircraftNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return aircraft

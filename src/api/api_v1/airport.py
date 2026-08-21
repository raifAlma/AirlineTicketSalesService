from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from starlette.responses import JSONResponse

from api.api_v1.fastapi_users import current_active_superuser
from api.dependencies.airport import create_airport_use_case, get_by_id_airport_use_case
from api.schemas.airport import ResponseAirportSchema, CreateAirportSchema
from infrastructure.database.postgresql.models import User, Airport
from infrastructure.repositories.postgres.airport.exception import AirportAlreadyExists
from infrastructure.types import AirportIdType
from usecases.airport.create_airport.abstract import AbstractCreateAirportUseCase
from usecases.airport.get_airport.abstract import AbstractGetAirportUseCase

router = APIRouter(
    prefix="/airport",
    tags=["Airport"],
)


@router.post('', response_model=ResponseAirportSchema, status_code=201)
async def create_airport(
        payload: CreateAirportSchema,
        usecase: AbstractCreateAirportUseCase = Depends(create_airport_use_case),
        _: User = Depends(current_active_superuser),
) -> JSONResponse:
    try:
        airport = await usecase.execute(payload)
    except AirportAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    return airport

@router.get('/{id}', response_model=ResponseAirportSchema, status_code=200)
async def get_airport(
        id: AirportIdType,
        usecase: AbstractGetAirportUseCase = Depends(get_by_id_airport_use_case),
        _: User = Depends(current_active_superuser),
) -> JSONResponse:
    airport = await usecase.execute(id)
    return airport
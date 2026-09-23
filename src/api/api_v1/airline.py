from fastapi import APIRouter, Depends, HTTPException, Query

from api.api_v1.fastapi_users import current_active_superuser
from api.dependencies.airline import create_airline_use_case
from api.schemas.airline import CreateAirlineSchema, ResponseCreateAirlineSchema
from domain.validators.airline.airline_exception import InvalidAirlineField
from infrastructure.database.postgresql.models import User
from infrastructure.repositories.postgres.airline.exception import AirlineAlreadyExists
from usecases.airline.create.abstract import AbstractCreateAirlineUseCase


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

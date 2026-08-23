
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from api.api_v1.fastapi_users import current_active_superuser
from api.dependencies.airport import create_airport_use_case, get_by_id_airport_use_case, search_airport_use_case, \
    delete_airport_use_case
from api.schemas.airport import CreateAirportSchema, ResponseAirportSchema
from infrastructure.database.postgresql.models import User
from infrastructure.repositories.postgres.airport.exception import AirportAlreadyExists, AirportNotFound
from infrastructure.types import AirportIdType
from usecases.airport.create.abstract import AbstractCreateAirportUseCase
from usecases.airport.get.abstract import AbstractGetAirportUseCase
from usecases.airport.search.abstract import AbstractSearchAirportUseCase
from usecases.airport.delete.abstract import AbstractDeleteAirportUseCase

router = APIRouter(
    prefix="/airport",
    tags=["Airport"],
)


@router.post("", response_model=ResponseAirportSchema, status_code=201)
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

@router.get("/search", response_model=list[ResponseAirportSchema])
async def search_airports(
    q: str = Query(..., min_length=1, max_length=100),
    usecase: AbstractSearchAirportUseCase = Depends(search_airport_use_case),
):
    return await usecase.execute(q)

@router.get("/{id}", response_model=ResponseAirportSchema, status_code=200)
async def get_airport(
    id: AirportIdType,
    usecase: AbstractGetAirportUseCase = Depends(get_by_id_airport_use_case),
    _: User = Depends(current_active_superuser),
) -> JSONResponse:
    try:
        airport = await usecase.execute(id)
    except AirportNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return airport

@router.delete("/{id}", status_code=204)
async def delete_airport(
        id: AirportIdType,
        usecase: AbstractDeleteAirportUseCase = Depends(delete_airport_use_case),
        _: User = Depends(current_active_superuser),
):
    try:
        await usecase.execute(id)
    except AirportNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None
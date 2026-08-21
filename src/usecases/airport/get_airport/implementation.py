from uuid import UUID

from fastapi import HTTPException

from infrastructure.database.postgresql.models import Airport
from infrastructure.types import AirportIdType
from usecases.airport.get_airport.abstract import AbstractGetAirportUseCase


class PostgreSQLGetAirportUseCase(AbstractGetAirportUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AirportIdType) -> Airport:
        async with self._uow as uow:
            airport = await uow.repository.get_by_id(id)
            if not airport:
                raise HTTPException(status_code=404, detail="Airport not found")
            return airport

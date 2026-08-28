from api.schemas.airport import UpdateAirportSchema
from infrastructure.database.postgresql.models import Airport
from infrastructure.types import AirportIdType
from usecases.airport.update.abstract import AbstractUpdateAirportUseCase
from domain.entities.airport import AirportUpdateData

class PostgreSQLUpdateAirportUseCase(AbstractUpdateAirportUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AirportIdType, payload: UpdateAirportSchema) -> Airport:
            data = AirportUpdateData(
                name=payload.name, code=payload.code, city=payload.city, country=payload.country
            )
            async with self._uow as uow:
                airport = await uow.repository.update( id ,data)
            return airport

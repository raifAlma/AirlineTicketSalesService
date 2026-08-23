from infrastructure.database.postgresql.models import Airport
from infrastructure.types import AirportIdType
from usecases.airport.get.abstract import AbstractGetAirportUseCase


class PostgreSQLGetAirportUseCase(AbstractGetAirportUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AirportIdType) -> Airport:
        async with self._uow as uow:
            airport = await uow.repository.get_by_id(id)
            return airport

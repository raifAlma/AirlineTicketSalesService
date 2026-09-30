from infrastructure.database.postgresql.models import Airline
from infrastructure.types import AirlineIdType
from usecases.airline.get_by_id.abstract import AbstractGetByIdAirlineUseCase


class PostgreSQLGetByIdAirlineUseCase(AbstractGetByIdAirlineUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AirlineIdType) -> Airline:
        async with self._uow as uow:
            airline = await uow.repository.get_by_id(id)
            return airline

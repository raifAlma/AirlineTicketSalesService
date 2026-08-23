from typing import List

from infrastructure.database.postgresql.models import Airport
from usecases.airport.search.abstract import AbstractSearchAirportUseCase


class PostgreSQLSearchAirportUseCase(AbstractSearchAirportUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, query: str) -> List[Airport]:
        async with self._uow as uow:
            airport = await uow.repository.search(query)
            return List(airport)

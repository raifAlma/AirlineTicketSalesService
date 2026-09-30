from typing import List

from infrastructure.database.postgresql.models import Airline
from usecases.airline.search.abstract import AbstractSearchAirlineUseCase


class PostgreSQLSearchAirlineUseCase(AbstractSearchAirlineUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, query: str) -> List[Airline]:
        async with self._uow as uow:
            airline = await uow.repository.search(query)
            return airline

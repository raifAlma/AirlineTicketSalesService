from typing import List

from infrastructure.database.postgresql.models import Aircraft
from usecases.aircraft.search.abstract import AbstractSearchAircraftUseCase


class PostgreSQLSearchAircraftUseCase(AbstractSearchAircraftUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, query: str) -> List[Aircraft]:
        async with self._uow as uow:
            aircraft = await uow.repository.search(query)
            return aircraft

from infrastructure.types import AirportIdType
from usecases.airport.delete.abstract import AbstractDeleteAirportUseCase


class PostgreSQLDeleteAirportUseCase(AbstractDeleteAirportUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AirportIdType) -> None:
        async with self._uow as uow:
            await uow.repository.delete(id)

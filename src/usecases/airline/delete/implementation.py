from infrastructure.types import AirlineIdType
from usecases.airline.delete.abstract import AbstractDeleteAirlineUseCase


class PostgreSQLDeleteAirlineseCase(AbstractDeleteAirlineUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AirlineIdType) -> None:
        async with self._uow as uow:
            await uow.repository.delete(id)

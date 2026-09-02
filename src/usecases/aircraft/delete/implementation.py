from infrastructure.types import AircraftIdType
from usecases.aircraft.delete.abstract import AbstractDeleteAircraftUseCase


class PostgreSQLDeleteAircraftUseCase(AbstractDeleteAircraftUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AircraftIdType) -> None:
        async with self._uow as uow:
            await uow.repository.delete(id)

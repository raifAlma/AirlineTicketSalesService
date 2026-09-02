from infrastructure.database.postgresql.models import Aircraft
from infrastructure.types import AircraftIdType
from usecases.aircraft.get.abstract import AbstractGetAircraftUseCase


class PostgreSQLGetAircraftUseCase(AbstractGetAircraftUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AircraftIdType) -> Aircraft:
        async with self._uow as uow:
            aircraft = await uow.repository.get_by_id(id)
            return aircraft

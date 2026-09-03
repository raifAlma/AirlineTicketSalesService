from domain.entities.aircraft import AircraftUpdateData
from infrastructure.types import AirportIdType
from usecases.aircraft.update.abstract import AbstractAircraftUpdateUseCase


class PostgreSQLUpdateAircraftUseCase(AbstractAircraftUpdateUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AirportIdType, payload: AircraftUpdateData):
        data = AircraftUpdateData(
            model=payload.model,
            rows=payload.rows,
            seats_per_row=payload.seats_per_row,
            business_rows=payload.business_rows,
        )
        async with self._uow as uow:
            aircraft = await uow.aircraft.update(id, data)
        return aircraft
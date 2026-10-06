from domain.entities.airline import AirlineUpdateData
from infrastructure.types import AirlineIdType
from usecases.airline.update.abstract import AbstractAirlineUpdateUseCase


class PostgreSQLUpdateAirlineUseCase(AbstractAirlineUpdateUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, id: AirlineIdType, payload: AirlineUpdateData):
        data = AirlineUpdateData(
            name=payload.name,
            iata_code=payload.iata_code,
            country=payload.country,
        )
        async with self._uow as uow:
            airline = await uow.repository.update(id, data)
        return airline

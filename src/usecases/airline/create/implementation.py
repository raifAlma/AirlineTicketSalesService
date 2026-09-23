from api.schemas.airline import CreateAirlineSchema
from domain.entities.airline import AirlineCreateData
from usecases.airline.create.abstract import (
    AbstractCreateAirlineUseCase,
)


class PostgreSQLCreateAirlineUseCase(AbstractCreateAirlineUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CreateAirlineSchema):
        data = AirlineCreateData(
            name=schema.name,
            iata_code=schema.iata_code,
            country=schema.country,
        )
        async with self._uow as uow:
            airline = await uow.repository.create(data)
        return airline

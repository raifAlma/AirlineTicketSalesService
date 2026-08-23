from api.schemas.airport import CreateAirportSchema
from domain.entities import AirportCreateData
from usecases.airport.create.abstract import (  # ← путь №3, вообще другой
    AbstractCreateAirportUseCase,
)


class PostgreSQLCreateAirportUseCase(AbstractCreateAirportUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CreateAirportSchema):
        data = AirportCreateData(
            name=schema.name, code=schema.code, city=schema.city, country=schema.country
        )
        async with self._uow as uow:
            airport = await uow.repository.create(data)
        return airport

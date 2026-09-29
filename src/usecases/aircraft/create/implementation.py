from api.schemas.aircraft import CreateAircraftSchema
from domain.entities.aircraft import AircraftCreateData
from infrastructure.types import AirlineIdType
from usecases.aircraft.create.abstract import (
    AbstractCreateAircraftUseCase,
)


class PostgreSQLCreateAircraftUseCase(AbstractCreateAircraftUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, airline_id: AirlineIdType, schema: CreateAircraftSchema):
        data = AircraftCreateData(
            model=schema.model,
            rows=schema.rows,
            seats_per_row=schema.seats_per_row,
            business_rows=schema.business_rows,
            tail_number=schema.tail_number,
            airline_id=airline_id,
        )
        async with self._uow as uow:
            aicraft = await uow.repository.create(airline_id, data)
        return aicraft

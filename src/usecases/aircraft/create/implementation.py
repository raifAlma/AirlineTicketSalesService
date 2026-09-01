from api.schemas.aircraft import CreateAircraftSchema
from domain.entities.aircraft import AircraftCreateData
from usecases.aircraft.create.abstract import (
    AbstractCreateAircraftUseCase,
)


class PostgreSQLCreateAircraftUseCase(AbstractCreateAircraftUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CreateAircraftSchema):
        data = AircraftCreateData(
            model=schema.model, rows=schema.rows,
            seats_per_row=schema.seats_per_row, business_rows=schema.business_rows
        )
        async with self._uow as uow:
            aicraft = await uow.repository.create(data)
        return aicraft

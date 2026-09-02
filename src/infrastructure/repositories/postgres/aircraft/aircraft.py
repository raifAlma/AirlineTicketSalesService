from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.abstract_repositories.aircraft import AbstractAircraftRepository
from domain.entities.aircraft import AircraftCreateData
from infrastructure.database.postgresql.models import Aircraft
from infrastructure.repositories.postgres.aircraft.exception import AircraftAlreadyExists, AircraftNotFound
from infrastructure.types import AircraftIdType


class PostgreSQLAircraftRepository(AbstractAircraftRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: AircraftCreateData):
        smt = select(Aircraft).where(Aircraft.model == payload.model)
        result = await self.session.execute(smt)
        existing_aircraft = result.scalar_one_or_none()
        if existing_aircraft:
            raise AircraftAlreadyExists(model=payload.model)
        aircraft = Aircraft(
            model=payload.model,
            rows = payload.rows,
            seats_per_row = payload.seats_per_row,
            business_rows = payload.business_rows,
        )
        self.session.add(aircraft)
        await self.session.flush()
        return aircraft

    async def get_by_id(self, id: AircraftIdType) -> Aircraft:
        smt = select(Aircraft).where(Aircraft.id == id)
        result = await self.session.execute(smt)
        aircraft = result.scalar_one_or_none()
        if not aircraft:
            raise AircraftNotFound(id=id)
        return aircraft

    async def search(self, query: str) -> List[Aircraft]:
        pattern = f"%{query}%"
        smt = select(Aircraft).where(Aircraft.model.ilike(pattern))
        result = await self.session.execute(smt)
        aircraft = result.scalars().all()
        return aircraft

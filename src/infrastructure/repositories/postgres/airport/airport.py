from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.airport import CreateAirportSchema
from domain.abstract_repositories.airport import AbstractAirportRepository
from infrastructure.database.postgresql.models import Airport
from infrastructure.repositories.postgres.airport.exception import AirportAlreadyExists
from infrastructure.types import AirportIdType


class PostgreSQLAirportRepository(AbstractAirportRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: CreateAirportSchema) -> Airport:
        smt = select(Airport).where(Airport.code == payload.code)
        res = await self.session.execute(smt)
        existing_airport = res.scalar_one_or_none()
        if existing_airport:
            raise AirportAlreadyExists()

        airport = Airport(
            code=payload.code,
            name=payload.name,
            city=payload.city,
            country=payload.country,
        )
        self.session.add(airport)
        await self.session.flush()
        return airport

    async def get_by_id(self, id: AirportIdType) -> Airport:
        smt = select(Airport).where(Airport.id == id)
        res = await self.session.execute(smt)
        airport = res.scalar_one_or_none()
        if airport is None:
            raise HTTPException(status_code=404, detail="Airport not found")
        return airport

from dataclasses import asdict
from typing import List

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.airport import CreateAirportSchema, UpdateAirportSchema
from domain.abstract_repositories.airport import AbstractAirportRepository
from domain.entities import AirportUpdateData
from infrastructure.database.postgresql.models import Airport
from infrastructure.repositories.postgres.airport.exception import (
    AirportAlreadyExists,
    AirportNotFound,
    InvalidAirportData,
)
from infrastructure.types import AirportIdType


class PostgreSQLAirportRepository(AbstractAirportRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: CreateAirportSchema) -> Airport:
        smt = select(Airport).where(Airport.code == payload.code)
        res = await self.session.execute(smt)
        existing_airport = res.scalar_one_or_none()
        if existing_airport:
            raise AirportAlreadyExists(code=payload.code)

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
            raise AirportNotFound(airport_id=id)
        return airport

    async def search(self, query: str) -> List[Airport]:
        pattern = f"%{query}%"
        stmt = select(Airport).where(
            or_(
                Airport.name.ilike(pattern),
                Airport.city.ilike(pattern),
                Airport.code == query.upper(),
            )
        )
        result = await self.session.execute(stmt)
        airport = result.scalars().all()
        return airport

    async def delete(self, id: AirportIdType) -> None:
        smt = select(Airport).where(Airport.id == id)
        res = await self.session.execute(smt)
        airport = res.scalar_one_or_none()
        if airport is None:
            raise AirportNotFound(airport_id=id)
        await self.session.delete(airport)
        await self.session.flush()

    async def update(self, id: AirportIdType, payload: AirportUpdateData) -> Airport:
        stmt = select(Airport).where(Airport.id == id)
        res = await self.session.execute(stmt)
        airport = res.scalar_one_or_none()
        if not airport:
            raise AirportNotFound(id)

        update_data = {k: v for k, v in asdict(payload).items() if v is not None}
        if "code" in update_data:
            new_code = update_data["code"]
            exists = await self.session.scalar(
                select(1).where(Airport.code == new_code, Airport.id != id)
            )
            if exists:
                raise AirportAlreadyExists(code=new_code)

        for field, value in update_data.items():
            if hasattr(airport, field):
                setattr(airport, field, value)

        await self.session.flush()
        return airport

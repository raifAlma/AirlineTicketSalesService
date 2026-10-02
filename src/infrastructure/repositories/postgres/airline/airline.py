from dataclasses import asdict
from typing import List

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.abstract_repositories.airline import AbstractAirlineRepository
from domain.entities.airline import AirlineCreateData, AirlineUpdateData
from infrastructure.database.postgresql.models import Airline
from infrastructure.repositories.postgres.airline.exception import (
    AirlineAlreadyExists,
    AirlineNotFound,
)
from infrastructure.types import AirlineIdType


class PostgreSQLAirlineRepository(AbstractAirlineRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: AirlineCreateData):
        smt = select(Airline).where(Airline.iata_code == payload.iata_code)
        result = await self.session.execute(smt)
        exists_iata_code = result.scalar_one_or_none()
        if exists_iata_code:
            raise AirlineAlreadyExists(iata_code=payload.iata_code)
        airline = Airline(
            name=payload.name,
            iata_code=payload.iata_code,
            country=payload.country,
        )
        self.session.add(airline)
        await self.session.flush()
        return airline

    async def get_by_id(self, id: AirlineIdType):
        smt = select(Airline).where(Airline.id == id)
        result = await self.session.execute(smt)
        airline = result.scalar_one_or_none()
        if airline is None:
            raise AirlineNotFound(id=id)
        return airline

    async def search(self, query: str) -> List[Airline]:
        pattern = f"%{query}%"
        smt = select(Airline).where(
            or_(
                Airline.iata_code == query.upper(),
                Airline.name.ilike(pattern),
                Airline.country.ilike(pattern),
            )
        )
        result = await self.session.execute(smt)
        airline = result.scalars().all()
        return airline

    async def delete(self, id: AirlineIdType):
        smt = select(Airline).where(Airline.id == id)
        result = await self.session.execute(smt)
        airline = result.scalar_one_or_none()
        if airline is None:
            raise AirlineNotFound(id=id)
        await self.session.delete(airline)
        await self.session.flush()


    async def update(self, id: AirlineIdType, payload: AirlineUpdateData):
        smt = select(Airline).where(Airline.id == id)
        result = await self.session.execute(smt)
        airline = result.scalar_one_or_none()
        if airline is None:
            raise AirlineNotFound(id=id)

        update_data = {k:v for k,v in asdict(payload).items() if v is not None}
        if 'iata_code' in update_data:
            new_iata_code = update_data['iata_code']
            existing_iata_code = await self.session.scalar(
                select(Airline).where(Airline.iata_code == new_iata_code, Airline.id != id)
            )
            if existing_iata_code:
                raise AirlineAlreadyExists(iata_code=new_iata_code)
            for field, value in update_data.items():
                if hasattr(airline, field):
                    setattr(airline, field, value)

            await self.session.flush()
            return airline
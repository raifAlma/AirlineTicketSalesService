from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from domain.abstract_repositories.airline import AbstractAirlineRepository
from domain.entities.airline import AirlineCreateData
from infrastructure.database.postgresql.models import Airline
from infrastructure.repositories.postgres.airline.exception import AirlineAlreadyExistsError


class PostgreSQLAirlineRepository(AbstractAirlineRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: AirlineCreateData):
        smt = select(Airline).where(
            Airline.iata_code == payload.iata_code
        )
        result = await self.session.execute(smt)
        exists_iata_code = result.scalar_one_or_none()
        if exists_iata_code:
            raise AirlineAlreadyExistsError(iata_code=payload.iata_code)
        airline = Airline(
            name=payload.name,
            iata_code=payload.iata_code,
            country=payload.country,
        )
        self.session.add(airline)
        await self.session.flush()
        return airline

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.airport.shemas import CreateAirportShema
from domain.abstract_repositories.airport import AbstractAirportRepository
from infrastructure.database.postgresql.models import Airport
from infrastructure.repositories.postgres.airport.exception import AirportAlreadyExists


class PostgreSQLAirportRepository(AbstractAirportRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: CreateAirportShema) -> Airport:
        smt = select(Airport).where(Airport.code == payload.code)
        res = self.session.execute(smt)
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
        await self.session.commit()
        return airport
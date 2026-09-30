from abc import ABC, abstractmethod

from infrastructure.database.postgresql.models import Airline
from infrastructure.types import AirlineIdType


class AbstractGetByIdAirlineUseCase(ABC):
    @abstractmethod
    async def execute(self, id: AirlineIdType) -> Airline: ...

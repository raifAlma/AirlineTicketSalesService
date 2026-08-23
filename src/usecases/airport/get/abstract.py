from abc import ABC, abstractmethod
from uuid import UUID

from infrastructure.database.postgresql.models import Airport
from infrastructure.types import AirportIdType


class AbstractGetAirportUseCase(ABC):
    @abstractmethod
    async def execute(self, id: AirportIdType) -> Airport: ...

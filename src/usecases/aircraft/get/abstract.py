from abc import ABC, abstractmethod

from infrastructure.database.postgresql.models import Aircraft
from infrastructure.types import AircraftIdType


class AbstractGetAircraftUseCase(ABC):
    @abstractmethod
    async def execute(self, id: AircraftIdType) -> Aircraft: ...

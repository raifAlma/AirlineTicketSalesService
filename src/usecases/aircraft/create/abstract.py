from abc import ABC, abstractmethod

from domain.entities.aircraft import AircraftCreateData
from infrastructure.types import AirlineIdType


class AbstractCreateAircraftUseCase(ABC):
    @abstractmethod
    async def execute(self, airline_id: AirlineIdType, schema: AircraftCreateData): ...

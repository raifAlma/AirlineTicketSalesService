from abc import ABC, abstractmethod

from domain.entities import AirportCreateData

class AbstractCreateAirportUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: AirportCreateData): ...
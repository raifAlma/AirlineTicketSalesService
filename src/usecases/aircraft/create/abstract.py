from abc import ABC, abstractmethod

from domain.entities.aircraft import AircraftCreateData


class AbstractCreateAircraftUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: AircraftCreateData): ...

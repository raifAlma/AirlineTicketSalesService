from abc import ABC, abstractmethod

from domain.entities.airline import AirlineCreateData


class AbstractCreateAirlineUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: AirlineCreateData): ...

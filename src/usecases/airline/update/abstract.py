from abc import ABC, abstractmethod

from domain.entities.airline import AirlineUpdateData
from infrastructure.types import AirlineIdType


class AbstractAirlineUpdateUseCase(ABC):
    @abstractmethod
    async def execute(self, id: AirlineIdType, payload: AirlineUpdateData): ...

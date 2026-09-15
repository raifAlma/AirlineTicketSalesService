from abc import ABC, abstractmethod

from domain.entities.aircraft import AircraftUpdateData
from infrastructure.types import AircraftIdType


class AbstractAircraftUpdateUseCase(ABC):
    @abstractmethod
    async def execute(self, id: AircraftIdType, payload: AircraftUpdateData): ...
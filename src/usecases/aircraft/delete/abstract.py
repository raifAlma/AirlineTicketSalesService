from abc import ABC, abstractmethod

from infrastructure.types import AirportIdType


class AbstractDeleteAircraftUseCase(ABC):
    @abstractmethod
    async def execute(self, id: AirportIdType) -> None: ...

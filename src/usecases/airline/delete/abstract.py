from abc import ABC, abstractmethod

from infrastructure.types import AirlineIdType


class AbstractDeleteAirlineUseCase(ABC):
    @abstractmethod
    async def execute(self, id: AirlineIdType) -> None: ...

from abc import ABC, abstractmethod
from typing import List

from infrastructure.database.postgresql.models import Airport

class AbstractSearchAirportUseCase(ABC):
    @abstractmethod
    async def execute(self, query: str) -> List[Airport]: ...

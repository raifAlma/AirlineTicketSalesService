from abc import ABC, abstractmethod
from typing import List

from infrastructure.database.postgresql.models import Airline


class AbstractSearchAirlineUseCase(ABC):
    @abstractmethod
    async def execute(self, query: str) -> List[Airline]: ...

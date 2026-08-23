from abc import ABC, abstractmethod
from typing import List

from domain.entities import AirportCreateData
from infrastructure.database.postgresql.models import Airport
from infrastructure.types import AirportIdType


class AbstractAirportRepository(ABC):

    @abstractmethod
    def create(self, payload: AirportCreateData) -> Airport:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: AirportIdType) -> Airport:
        raise NotImplementedError

    @abstractmethod
    def search (self, query: str) -> List[Airport]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: AirportIdType) -> None:
        raise NotImplementedError

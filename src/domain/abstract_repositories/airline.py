from abc import ABC, abstractmethod
from typing import List

from domain.entities.airline import AirlineCreateData, AirlineUpdateData
from infrastructure.database.postgresql.models import Airline
from infrastructure.types import AirlineIdType


class AbstractAirlineRepository(ABC):

    @abstractmethod
    async def create(self, payload: AirlineCreateData) -> Airline:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: AirlineIdType) -> Airline:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: str) -> List[Airline]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: AirlineIdType) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: AirlineIdType, data: AirlineUpdateData):
        raise NotImplementedError
from abc import ABC, abstractmethod
from typing import List

from domain.entities.aircraft import AircraftCreateData
from infrastructure.database.postgresql.models import Aircraft
from infrastructure.types import AircraftIdType


class AbstractAircraftRepository(ABC):

    @abstractmethod
    async def create(self, payload: AircraftCreateData) -> Aircraft:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: AircraftIdType) -> Aircraft:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: str) -> List[Aircraft]:
        raise NotImplementedError
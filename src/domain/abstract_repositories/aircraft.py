from abc import ABC, abstractmethod

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

from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities import AirportCreateData
from infrastructure.database.postgresql.models import Airport
from infrastructure.types import AirportIdType


class AbstractAirportRepository(ABC):

    @abstractmethod
    def create(self, payload: AirportCreateData) -> Airport:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: AirportIdType ) -> Airport:
        raise NotImplementedError
from abc import ABC, abstractmethod

from domain.entities import AirportCreateData
from infrastructure.database.postgresql.models import Airport


class AbstractAirportRepository(ABC):

    @abstractmethod
    def create(self, payload: AirportCreateData) -> Airport:
        raise NotImplementedError


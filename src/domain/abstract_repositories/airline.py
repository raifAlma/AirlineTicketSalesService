from abc import ABC, abstractmethod

from domain.entities.airline import AirlineCreateData
from infrastructure.database.postgresql.models import Airline


class AbstractAirlineRepository(ABC):

    @abstractmethod
    async def create (self, payload: AirlineCreateData) -> Airline:
        raise NotImplementedError
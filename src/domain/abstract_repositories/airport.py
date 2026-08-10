from abc import ABC, abstractmethod

from api.api_v1.airport.shemas import CreateAirportShema
from infrastructure.database.postgresql.models import Airport


class AbstractAirportRepository(ABC):

    @abstractmethod
    def create(self, payload: CreateAirportShema) -> Airport:
        raise NotImplementedError


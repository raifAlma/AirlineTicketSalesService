from abc import ABC, abstractmethod

from domain.entities.aircraft import AircraftCreateData


class AbstractAircraftRepository(ABC):

    @abstractmethod
    async def create(self, payload: AircraftCreateData):
        raise NotImplementedError

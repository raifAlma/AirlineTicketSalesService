from abc import ABC, abstractmethod

from domain.entities.aircraft import AircraftCreateData


class AbstractAircraftRepository(ABC):

    @abstractmethod
    def create(self, payload: AircraftCreateData):
        raise NotImplementedError

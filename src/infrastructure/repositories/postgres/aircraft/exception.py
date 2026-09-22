from infrastructure.types import AircraftIdType


class AircraftError(Exception):
    """Базовое исключение для всех ошибок, связанных с Airport."""

    pass


class AircraftAlreadyExists(AircraftError):
    def __init__(self, tail_number: str | None = None):
        self.name = tail_number
        message = (
            f"Aircraft with tail_number {tail_number!r} already exists"
            if tail_number
            else "Aircraft already exists, check the entered data"
        )
        super().__init__(message)


class AircraftNotFound(AircraftError):
    def __init__(self, id: AircraftIdType | None = None):
        self.id = id
        message = f"Aircraft with id {id!r} does not exist"
        super().__init__(message)

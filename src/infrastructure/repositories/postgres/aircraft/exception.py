class AircraftError(Exception):
    """Базовое исключение для всех ошибок, связанных с Airport."""

    pass


class AircraftAlreadyExists(AircraftError):
    def __init__(self, model: str | None = None):
        self.name = model
        message = (
            f"Aircraft with model {model!r} already exists"
            if model
            else "Aircraft already exists, check the entered data"
        )
        super().__init__(message)
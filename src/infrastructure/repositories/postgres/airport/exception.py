class AirportError(Exception):
    """Базовое исключение для всех ошибок, связанных с Airport."""

    pass


class AirportAlreadyExists(AirportError):
    def __init__(self, code: str | None = None):
        self.code = code
        message = (
            f"Airport with code {code!r} already exists"
            if code
            else "Airport already exists, check the entered data"
        )
        super().__init__(message)


class AirportNotFound(AirportError):
    def __init__(self, airport_id):
        self.airport_id = airport_id
        super().__init__(f"Airport with id {airport_id!r} not found")


class InvalidAirportData(AirportError):
    def __init__(self):
        super().__init__("Invalid Airport data, check the entered data")

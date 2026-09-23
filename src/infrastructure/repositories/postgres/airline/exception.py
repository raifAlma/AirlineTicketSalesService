class AirlineError(Exception):
    pass


class AirlineAlreadyExists(AirlineError):
    def __init__(self, iata_code: str):
        self.iata_code = iata_code
        message = f"Airline with code {self.iata_code} already exists."
        super().__init__(message)

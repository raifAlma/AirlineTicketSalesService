from dataclasses import dataclass

class InvalidAircraftName(ValueError):
    pass

class InvalidQuantityBusinessRows(ValueError):
    pass

@dataclass
class AircraftCreateData:
    model: str
    rows: int
    seats_per_row: int
    business_rows: int

    def __post_init__(self):
        self._validate_model()
        self._validate_business_rows()

    def _validate_model(self):
        if 1 > len(self.model) > 100:
            raise InvalidAircraftName(
                f"Invalid Aircraft model name. Must be between 1 and 100. Got {len(self.model)}"
            )

    def _validate_business_rows(self):
        if self.business_rows > self.rows:
            raise InvalidQuantityBusinessRows(
                f"business_rows ({self.business_rows}) cannot exceed rows ({self.rows})"
            )


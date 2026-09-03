from dataclasses import dataclass

from domain.validators.aircraft import validate_business_rows, validate_model


@dataclass
class AircraftCreateData:
    model: str
    rows: int
    seats_per_row: int
    business_rows: int

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_per_row

    def __post_init__(self):
        validate_model(self.model)
        validate_business_rows(self.rows, self.business_rows)


@dataclass
class AircraftUpdateData:
    model: str | None
    rows: int | None
    seats_per_row: int | None
    business_rows: int | None

    def __post_init__(self):
        if self.model is not None:
            validate_model(self.model)
        if self.rows is not None and self.business_rows is not None:
            validate_business_rows(self.rows, self.business_rows)

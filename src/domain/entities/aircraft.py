from dataclasses import dataclass

from domain.validators.aircraft.aircraft import (
    validate_model,
    validate_tail_number,
    validate_rows,
    validate_seats_per_row,
    validate_business_rows,
)


@dataclass
class AircraftCreateData:
    model: str
    rows: int
    seats_per_row: int
    business_rows: int
    tail_number: str

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_per_row

    def __post_init__(self):
        validate_tail_number(self.tail_number)
        validate_model(self.model)
        validate_rows(self.rows)
        validate_seats_per_row(self.seats_per_row)
        validate_business_rows(self.rows, self.business_rows)


@dataclass
class AircraftUpdateData:
    model: str | None = None
    rows: int | None = None
    seats_per_row: int | None = None
    business_rows: int | None = None
    tail_number: str | None = None

    def __post_init__(self):
        validate_tail_number(self.tail_number)
        validate_model(self.model)
        validate_rows(self.rows)
        validate_seats_per_row(self.seats_per_row)
        validate_business_rows(self.rows, self.business_rows)
from domain.validators.aircraft.aircraft_exceptions import (
    InvalidModelName,
    InvalidQuantityBusinessRows,
    InvalidQuantityRows,
    InvalidSeatsPerRow,
    InvalidTailNumber,
)


def validate_model(model: str) -> None:
    if model is None:
        return
    if not (1 <= len(model) <= 100):
        raise InvalidModelName(
            f"Invalid Aircraft model name. Must be between 1 and 100. Got {len(model)}"
        )


def validate_tail_number(tail_number: str) -> None:
    if tail_number is None:
        return
    if not (1 <= len(tail_number) <= 20):
        raise InvalidTailNumber(
            f"Invalid tail_number. Must be between 1 and 20. Got {len(tail_number)}"
        )


def validate_rows(rows: int) -> None:
    if rows is None:
        return
    if not (1 <= rows <= 100):
        raise InvalidQuantityRows(
            f"Invalid rows. Must be between 1 and 100. Got {rows}"
        )


def validate_seats_per_row(seats_per_row: int) -> None:
    if seats_per_row is None:
        return
    if not (1 <= seats_per_row <= 10):
        raise InvalidSeatsPerRow(
            f"Invalid seats_per_row. Must be between 1 and 10. Got {seats_per_row}"
        )


def validate_business_rows(rows: int, business_rows: int) -> None:
    if rows is None or business_rows is None:
        return
    if business_rows < 0:
        raise InvalidQuantityBusinessRows("business_rows cannot be negative")
    if business_rows > rows:
        raise InvalidQuantityBusinessRows(
            f"business_rows ({business_rows}) cannot exceed rows ({rows})"
        )

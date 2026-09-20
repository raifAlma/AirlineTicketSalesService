class InvalidAircraftName(ValueError):
    pass


class InvalidQuantityBusinessRows(ValueError):
    pass


def validate_model(model: str):
    if not (1 <= len(model) <= 100):
        raise InvalidAircraftName(
            f"Invalid Aircraft model name. Must be between 1 and 100. Got {len(model)}"
        )


def validate_business_rows(rows: int, business_rows: int):
    if rows is None or business_rows is None:
        return
    if business_rows < 0:
        raise InvalidQuantityBusinessRows("business_rows cannot be negative")
    if business_rows > rows:
        raise InvalidQuantityBusinessRows(
            f"business_rows ({business_rows}) cannot exceed rows ({rows})"
        )

class InvalidAircraftName(ValueError):
    pass


class InvalidQuantityBusinessRows(ValueError):
    pass


def validate_model(self):
    if not (1 <= len(self.model) <= 100):
        raise InvalidAircraftName(
            f"Invalid Aircraft model name. Must be between 1 and 100. Got {len(self.model)}"
        )


def validate_business_rows(self):
    if self.business_rows > self.rows:
        raise InvalidQuantityBusinessRows(
            f"business_rows ({self.business_rows}) cannot exceed rows ({self.rows})"
        )

class InvalidAircraftField(ValueError):
    pass


class InvalidModelName(InvalidAircraftField):
    pass


class InvalidTailNumber(InvalidAircraftField):
    pass


class InvalidQuantityRows(InvalidAircraftField):
    pass


class InvalidSeatsPerRow(InvalidAircraftField):
    pass


class InvalidQuantityBusinessRows(InvalidAircraftField):
    pass
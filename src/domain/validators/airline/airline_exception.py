class InvalidAirlineField(ValueError):
    pass


class InvalidAirlineName(InvalidAirlineField):
    pass


class InvalidAirlineCountry(InvalidAirlineField):
    pass


class InvalidIataCode(InvalidAirlineField):
    pass

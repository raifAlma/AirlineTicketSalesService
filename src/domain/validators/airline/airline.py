from .airline_exception import (
    InvalidAirlineCountry,
    InvalidAirlineName,
    InvalidIataCode,
)


def validate_airline_name(name: str):
    if name is None:
        return
    if not (1 <= len(name) <= 100):
        raise InvalidAirlineName(
            f"Airline name must be between 1 and 100 characters, got {len(name)}"
        )


def validate_airline_county(county: str):
    if county is None:
        return
    if not (1 <= len(county) <= 100):
        raise InvalidAirlineCountry(
            f"County must be between 1 and 100 characters, got {len(county)}"
        )


def validate_iata_code(code: str):
    if code is None:
        return
    if not (1 <= len(code) <= 3 and code.isalpha() and code.isupper()):
        raise InvalidIataCode(
            f"Iata code must be exactly 3 uppercase letters, got {code!r}"
        )

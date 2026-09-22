class InvalidAirlineName(Exception):
    pass

class InvalidAirlineCounty(Exception):
    pass

class InvalidIataCode(Exception):
    pass

def validate_airline_name(name: str):
    if not (1 <= len(name) <= 100):
        raise InvalidAirlineName(
            f'Airline name must be between 1 and 100 characters, got {len(name)}'
        )

def validate_airline_county(county: str):
    if not (1 <= len(county) <= 100):
        raise InvalidAirlineCounty(
            f'County must be between 1 and 100 characters, got {len(county)}'
        )

def validate_iata_code(code: str):
    if not (1 <= len(code) <= 3 and code.isalpha() and code.isupper()):
        raise InvalidIataCode(
            f'Iata code must be exactly 3 uppercase letters, got {code!r}'
        )
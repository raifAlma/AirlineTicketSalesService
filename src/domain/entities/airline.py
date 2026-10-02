from dataclasses import dataclass

from domain.validators.airline.airline import (
    validate_airline_county,
    validate_airline_name,
    validate_iata_code,
)


@dataclass
class AirlineCreateData:
    name: str
    iata_code: str
    country: str

    def __post_init__(self):
        validate_airline_name(self.name)
        validate_airline_county(self.country)
        validate_iata_code(self.iata_code)

@dataclass
class AirlineUpdateData:
    name: str|None = None
    iata_code: str|None = None
    country: str|None = None

    def __post_init__(self):
        validate_airline_name(self.name)
        validate_airline_county(self.country)
        validate_iata_code(self.iata_code)

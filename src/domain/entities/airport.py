from dataclasses import dataclass

@dataclass
class AirportCreateData:
    code: str
    name: str
    city: str
    country: str

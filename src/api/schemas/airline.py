from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict

from infrastructure.types import AirlineIdType


def validate_iata_code(v: str | None) -> str | None:
    if v is None:
        return v
    if not (len(v) == 3 and v.isupper() and v.isalpha()):
        raise ValueError("Airline code must be exactly 3 uppercase letters")
    return v


class CreateAirlineSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    iata_code: str
    country: str = Field(min_length=1, max_length=100)

    @field_validator("iata_code")
    @classmethod
    def create_validate_iata_code(cls, v):
        return validate_iata_code(v)

class ResponseCreateAirlineSchema(CreateAirlineSchema):
    id: AirlineIdType
    model_config = ConfigDict(from_attributes=True)
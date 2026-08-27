from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict


def validate_code(v: str | None) -> str | None:
    if v is None:
        return v
    if not (len(v) == 3 and v.isalpha() and v.isupper()):
        raise ValueError(f"Airport code must be exactly 3 uppercase letters")
    return v


class CreateAirportSchema(BaseModel):
    code: str
    name: str = Field(min_length=3, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=3, max_length=100)

    @field_validator("code")
    @classmethod
    def create_validate_code(cls, v):
        return validate_code(v)


class ResponseAirportSchema(CreateAirportSchema):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class UpdateAirportSchema(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

    @field_validator("code")
    @classmethod
    def update_validate_code(cls, v):
        return validate_code(v)
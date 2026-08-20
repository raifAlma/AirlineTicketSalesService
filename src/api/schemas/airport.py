from pydantic import BaseModel, field_validator, ValidationError, Field


class CreateAirportSchema(BaseModel):
    code: str
    name: str = Field(min_length=3, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=3, max_length=100)

    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        if not (len(v) == 3 and v.isalpha() and v.isupper()):
            raise ValueError(
                f"Airport code must be exactly 3 uppercase letters")
        return v

class ResponseAirportSchema(CreateAirportSchema):
    pass
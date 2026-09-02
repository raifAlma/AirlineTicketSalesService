from uuid import UUID

from pydantic import BaseModel, Field, model_validator, computed_field, ConfigDict


class CreateAircraftSchema(BaseModel):
    model: str = Field(min_length=1, max_length=100)
    rows: int = Field(gt=0, le=100)
    seats_per_row: int = Field(gt=0, le=10)
    business_rows: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_business_rows(self) -> "CreateAircraftSchema":
        if self.business_rows > self.rows:
            raise ValueError(
                f"business_rows ({self.business_rows}) cannot exceed rows ({self.rows})"
            )
        return self

class ResponseAircraftSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    model: str
    rows: int
    seats_per_row: int
    business_rows: int
    @computed_field
    @property
    def capacity(self) -> int:
        return self.rows * self.seats_per_row

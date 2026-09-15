from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


def validate_business_rows(model) -> None:
    business_rows = model.business_rows
    rows = model.rows
    if rows is not None and business_rows is not None and business_rows > rows:
        raise ValueError(
            f"business_rows ({business_rows}) cannot exceed rows ({rows})"
        )

class CreateAircraftSchema(BaseModel):
    model: str = Field(min_length=1, max_length=100)
    rows: int = Field(gt=0, le=100)
    seats_per_row: int = Field(gt=0, le=10)
    business_rows: int = Field(ge=0)

    @model_validator(mode="after")
    def validate(self) -> 'CreateAircraftSchema':
        validate_business_rows(self)
        return self


class UpdateAircraftSchema(BaseModel):
    model: Optional[str] = None
    rows: Optional[int] = None
    seats_per_row: Optional[int] = None
    business_rows: Optional[int] = None

    @model_validator(mode='after')
    def validate(self) -> 'UpdateAircraftSchema':
        validate_business_rows(self)
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

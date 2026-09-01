from pydantic import BaseModel, Field, model_validator


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
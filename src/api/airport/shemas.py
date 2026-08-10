from pydantic.v1 import BaseModel


class CreateAirportShema(BaseModel):
    code: str
    name: str
    city: str
    country: str
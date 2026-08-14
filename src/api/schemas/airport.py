from pydantic import BaseModel




class CreateAirportSchema(BaseModel):
    code: str
    name: str
    city: str
    country: str

class ResponseAirportSchema(CreateAirportSchema):
    pass
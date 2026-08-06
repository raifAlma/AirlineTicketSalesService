from pydantic import BaseModel


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    resert_passwerd_token_secret: str
    verification_token_secret: str
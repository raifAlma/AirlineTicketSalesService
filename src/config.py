from pydantic import BaseModel


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    resert_password_token_secret: str
    verification_token_secret: str

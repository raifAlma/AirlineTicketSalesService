import uuid
from typing import Optional, Literal

from fastapi_users import schemas
from pydantic import Field, field_validator


def _validate_phone_format(v: str) -> str:
    if v.startswith('+'):
        v = v[1:]
    if not v.isdigit():
        raise ValueError("Номер телефона должен содержать только цифры (может начинаться с +)")
    if not (10 <= len(v) <= 15):
        raise ValueError("Номер телефона должен содержать от 10 до 15 цифр")
    return v

class UserRead(schemas.BaseUser[uuid.UUID]):
    full_name: str
    phone: str
    role: str

class UserCreate(schemas.BaseUserCreate):
    full_name: str = Field(min_length=3, max_length=100)
    phone: str

    @field_validator('phone')
    @classmethod
    def phone_validator(cls, v:str) -> str:
        return _validate_phone_format(v)

class UserUpdate(schemas.BaseUserUpdate):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[Literal["user", "admin"]] = None

    @field_validator('phone')
    @classmethod
    def phone_validator(cls, v: Optional[str]) -> Optional[str]:
      if v is None:
          return None
      return _validate_phone_format(v)
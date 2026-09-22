# airline.py
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .aircraft import Aircraft


class Airline(Base):
    __tablename__ = "airline"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    iata_code: Mapped[str] = mapped_column(String(4), nullable=False, unique=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    aircrafts: Mapped[list["Aircraft"]] = relationship(back_populates="airline")
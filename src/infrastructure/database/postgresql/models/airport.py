from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .flight import Flight
from ..base import Base

import uuid
from sqlalchemy.dialects.postgresql import UUID

class Airport(Base):
    __tablename__ = "airports"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    departures: Mapped[list["Flight"]] = relationship(
        'Flight', foreign_keys='Flight.departure_airport_id', back_populates='departure_airport'
    )
    arrivals: Mapped[list["Flight"]] = relationship(
        'Flight', foreign_keys='Flight.arrival_airport_id', back_populates='arrival_airport'
    )
import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import List

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class StatusType(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    DELAYED = "DELAYED"
    CANCELED = "CANCELED"


class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    aircraft_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("aircraft.id"), nullable=False
    )
    departure_airport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("airports.id"), nullable=False
    )
    arrival_airport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("airports.id"), nullable=False
    )

    arrival_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    status: Mapped[StatusType] = mapped_column(
        Enum(StatusType), nullable=False, default=StatusType.SCHEDULED
    )

    aircraft: Mapped["Aircraft"] = relationship(back_populates="flights")
    departure_airport: Mapped["Airport"] = relationship(
        "Airport",
        foreign_keys="Flight.departure_airport_id",
        back_populates="departures",
    )
    arrival_airport: Mapped["Airport"] = relationship(
        "Airport",
        foreign_keys="Flight.arrival_airport_id",
        back_populates="arrivals",
    )

    seats: Mapped[List["Seat"]] = relationship(
        back_populates="flight", cascade="all, delete-orphan"
    )
    bookings: Mapped[List["Booking"]] = relationship(back_populates="flight")

import enum
import uuid
from typing import List

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class SeatType(enum.Enum):
    ECONOMY = "Economy"
    BUSINESS = "Business"


class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    flight_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("flights.id"), nullable=False
    )
    seat_number: Mapped[str] = mapped_column(String(10), nullable=False)
    class_type: Mapped[SeatType] = mapped_column(Enum(SeatType), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    flight: Mapped["Flight"] = relationship(back_populates="seats")
    booking_seats: Mapped[List["BookingSeat"]] = relationship(back_populates="seat")

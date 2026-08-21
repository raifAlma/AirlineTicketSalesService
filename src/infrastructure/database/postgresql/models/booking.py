import enum
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class BookingStatusType(enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"


import uuid

from sqlalchemy.dialects.postgresql import UUID


class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    flight_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("flights.id"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="bookings")
    flight: Mapped["Flight"] = relationship(back_populates="bookings")
    booking_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    status: Mapped[BookingStatusType] = mapped_column(
        Enum(BookingStatusType), default=BookingStatusType.PENDING
    )
    booking_seats: Mapped[List["BookingSeat"]] = relationship(back_populates="booking")
    payment: Mapped["Payment"] = relationship(back_populates="booking")

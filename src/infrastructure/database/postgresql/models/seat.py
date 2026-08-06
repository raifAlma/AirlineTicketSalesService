import enum
from typing import List

from sqlalchemy import String, Integer, Boolean, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base

class SeatType(enum.Enum):
    ECONOMY = 'Economy'
    BUSINESS = 'Business'
    FIRST = 'First'


class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    flight_id: Mapped[int] = mapped_column(ForeignKey("flights.id"), nullable=False)
    seat_number: Mapped[str] = mapped_column(String(10), nullable=False)
    class_type: Mapped[SeatType] = mapped_column(Enum(SeatType), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    flight: Mapped['Flight'] = relationship(back_populates="seats")
    booking_seats: Mapped[List["BookingSeat"]] = relationship(back_populates="seat")
# src/infrastructure/database/postgresql/models/booking_seat.py
from sqlalchemy import Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base

class BookingSeat(Base):
    __tablename__ = "booking_seats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), nullable=False)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"), nullable=False)
    price_at_booking: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)

    booking: Mapped["Booking"] = relationship(back_populates="booking_seats")
    seat: Mapped["Seat"] = relationship(back_populates="booking_seats")
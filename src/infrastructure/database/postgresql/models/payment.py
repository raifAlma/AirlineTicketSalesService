import enum
import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from . import Booking


class PaymentsStatusType(enum.Enum):
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    status: Mapped[PaymentsStatusType] = mapped_column(
        Enum(PaymentsStatusType), nullable=False
    )
    payment_method: Mapped[str] = mapped_column(String, nullable=False)
    transaction_id: Mapped[int] = mapped_column(Integer, nullable=False)

    booking: Mapped["Booking"] = relationship(back_populates="payment")

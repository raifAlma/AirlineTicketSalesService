import uuid

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from .flight import Flight


class Aircraft(Base):
    __tablename__ = "aircraft"
    id: Mapped[uuid.UUID] = mapped_column(..., primary_key=True, default=uuid.uuid4)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    rows: Mapped[int] = mapped_column(Integer, nullable=False)
    seats_per_row: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    business_rows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # capacity можно вычислять: rows * seats_per_row
    flights: Mapped[list[Flight]] = relationship(back_populates="aircraft")
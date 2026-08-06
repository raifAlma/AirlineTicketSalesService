from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

from .flight import Flight
from ..base import Base


class Aircraft(Base):
    __tablename__ = "aircraft"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    flights: Mapped[list[Flight]] = relationship(back_populates="aircraft")
import datetime
import enum
import uuid
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import String, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

# passenger — обычный пассажир (просмотр своих бронирований, покупка билетов).
# manager — менеджер рейсов (управление рейсами, самолётами, просмотр всех бронирований).
# admin — администратор (то же, что менеджер, но плюс управление пользователями).


class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = "users"
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    role: Mapped[str] = mapped_column(String(128),
                                      Enum(UserRole),nullable=False, default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    bookings: Mapped[List['Booking']] = relationship(back_populates='user')



    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
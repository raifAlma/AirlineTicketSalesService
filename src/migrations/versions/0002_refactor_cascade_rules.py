"""refactor cascade rules

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-02 18:04:45.741355

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: Union[str, Sequence[str], None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Сначала создаём ENUM-тип в PostgreSQL
    userrole_enum = sa.Enum("USER", "ADMIN", name="userrole")
    userrole_enum.create(op.get_bind(), checkfirst=True)

    # 2. Затем меняем тип колонки.
    #    UPPER() приводит существующие значения ('user' -> 'USER') к значениям ENUM.
    op.alter_column(
        "users",
        "role",
        existing_type=sa.VARCHAR(length=128),
        type_=userrole_enum,
        existing_nullable=False,
        postgresql_using="upper(role::text)::userrole",
    )

    # 3. Операции с FK
    op.drop_constraint(
        "booking_seats_seat_id_fkey", "booking_seats", type_="foreignkey"
    )
    op.drop_constraint(
        "booking_seats_booking_id_fkey", "booking_seats", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_booking_seats_booking_id_bookings"),
        "booking_seats",
        "bookings",
        ["booking_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_booking_seats_seat_id_seats"),
        "booking_seats",
        "seats",
        ["seat_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint("bookings_user_id_fkey", "bookings", type_="foreignkey")
    op.drop_constraint("bookings_flight_id_fkey", "bookings", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_bookings_user_id_users"),
        "bookings",
        "users",
        ["user_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        op.f("fk_bookings_flight_id_flights"),
        "bookings",
        "flights",
        ["flight_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    op.drop_constraint("flights_aircraft_id_fkey", "flights", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_flights_aircraft_id_aircraft"),
        "flights",
        "aircraft",
        ["aircraft_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint("payments_booking_id_fkey", "payments", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_payments_booking_id_bookings"),
        "payments",
        "bookings",
        ["booking_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint("seats_flight_id_fkey", "seats", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_seats_flight_id_flights"),
        "seats",
        "flights",
        ["flight_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Откат FK-операций
    op.drop_constraint(op.f("fk_seats_flight_id_flights"), "seats", type_="foreignkey")
    op.create_foreign_key(
        "seats_flight_id_fkey", "seats", "flights", ["flight_id"], ["id"]
    )

    op.drop_constraint(
        op.f("fk_payments_booking_id_bookings"), "payments", type_="foreignkey"
    )
    op.create_foreign_key(
        "payments_booking_id_fkey", "payments", "bookings", ["booking_id"], ["id"]
    )

    op.drop_constraint(
        op.f("fk_flights_aircraft_id_aircraft"), "flights", type_="foreignkey"
    )
    op.create_foreign_key(
        "flights_aircraft_id_fkey", "flights", "aircraft", ["aircraft_id"], ["id"]
    )

    op.drop_constraint(
        op.f("fk_bookings_flight_id_flights"), "bookings", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_bookings_user_id_users"), "bookings", type_="foreignkey"
    )
    op.create_foreign_key(
        "bookings_flight_id_fkey", "bookings", "flights", ["flight_id"], ["id"]
    )
    op.create_foreign_key(
        "bookings_user_id_fkey", "bookings", "users", ["user_id"], ["id"]
    )

    op.drop_constraint(
        op.f("fk_booking_seats_seat_id_seats"), "booking_seats", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_booking_seats_booking_id_bookings"),
        "booking_seats",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "booking_seats_booking_id_fkey",
        "booking_seats",
        "bookings",
        ["booking_id"],
        ["id"],
    )
    op.create_foreign_key(
        "booking_seats_seat_id_fkey", "booking_seats", "seats", ["seat_id"], ["id"]
    )

    # 2. Возвращаем колонку к VARCHAR.
    #    lower() приводит 'USER' -> 'user', чтобы совпадало с прежним форматом данных.
    op.alter_column(
        "users",
        "role",
        existing_type=sa.Enum("USER", "ADMIN", name="userrole"),
        type_=sa.VARCHAR(length=128),
        existing_nullable=False,
        postgresql_using="lower(role::text)",
    )

    # 3. И только ПОСЛЕ этого удаляем ENUM-тип
    userrole_enum = sa.Enum("USER", "ADMIN", name="userrole")
    userrole_enum.drop(op.get_bind(), checkfirst=True)

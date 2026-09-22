"""fixed errors

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-11 15:51:31.877226

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "0003"
down_revision: Union[str, Sequence[str], None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------- 1. Исправление таблицы токенов ----------
    # Удалим старую таблицу с неправильным именем, если она существует
    op.execute("DROP TABLE IF EXISTS access_token CASCADE")

    # Создадим правильную таблицу accesstoken
    op.create_table(
        "accesstoken",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("token"),
    )
    op.create_index(
        op.f("ix_accesstoken_created_at"), "accesstoken", ["created_at"], unique=False
    )

    # ---------- 2. Добавление колонок в flights ----------
    # Создадим enum-тип, если его ещё нет
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statustype') THEN
                CREATE TYPE statustype AS ENUM ('SCHEDULED', 'DELAYED', 'CANCELED');
            END IF;
        END$$;
    """)

    # Добавляем колонки как nullable
    op.add_column("flights", sa.Column("arrival_time", sa.DateTime(), nullable=True))
    op.add_column(
        "flights", sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=True)
    )
    op.add_column(
        "flights",
        sa.Column(
            "status",
            sa.Enum(
                "SCHEDULED", "DELAYED", "CANCELED", name="statustype", create_type=False
            ),
            nullable=True,
        ),
    )
    # Важно: create_type=False, потому что тип мы уже создали вручную

    # Заполняем дефолтными значениями существующие записи
    op.execute(
        "UPDATE flights SET arrival_time = NOW(), price = 0.00, status = 'SCHEDULED'"
    )

    # Ставим NOT NULL
    op.alter_column("flights", "arrival_time", nullable=False)
    op.alter_column("flights", "price", nullable=False)
    op.alter_column("flights", "status", nullable=False)


def downgrade() -> None:
    # Удаляем колонки
    op.alter_column("flights", "arrival_time", nullable=True)
    op.alter_column("flights", "price", nullable=True)
    op.drop_column("flights", "status")
    # Удаляем enum-тип
    sa.Enum(name="statustype").drop(op.get_bind(), checkfirst=True)

    # Откат таблицы токенов: удаляем правильную и создаём старую
    op.drop_table("accesstoken")
    op.create_table(
        "access_token",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("token"),
    )
    op.create_index(
        op.f("ix_accesstoken_created_at"), "access_token", ["created_at"], unique=False
    )

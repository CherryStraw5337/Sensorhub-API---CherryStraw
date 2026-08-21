"""add status to existing alerts

Revision ID: b7e8f9a0c1d2
Revises: 6c2f4a9b7d10
Create Date: 2026-08-21 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


revision: str = "b7e8f9a0c1d2"
down_revision: str | Sequence[str] | None = "6c2f4a9b7d10"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _column_names(bind: sa.Connection, table_name: str) -> set[str]:
    if bind.dialect.name == "postgresql":
        rows = bind.execute(
            sa.text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = current_schema()
                  AND table_name = :table_name
                """
            ),
            {"table_name": table_name},
        )
        return {row[0] for row in rows}

    rows = bind.exec_driver_sql(f'PRAGMA table_info("{table_name}")')
    return {row[1] for row in rows}


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "alerts" not in inspector.get_table_names():
        return

    if "status" not in _column_names(bind, "alerts"):
        op.add_column(
            "alerts",
            sa.Column("status", sa.String(), server_default="open", nullable=False),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "alerts" in inspector.get_table_names() and "status" in _column_names(bind, "alerts"):
        op.drop_column("alerts", "status")
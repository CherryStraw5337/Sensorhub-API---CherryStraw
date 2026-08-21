"""completar el esquema con las columnas actuales de los modelos

Revision ID: 6c2f4a9b7d10
Revises: ad3f3d91ac12
Create Date: 2026-08-20 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


revision: str = "6c2f4a9b7d10"
down_revision: str | Sequence[str] | None = "ad3f3d91ac12"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("sensors", sa.Column("threshold", sa.Float(), nullable=True))
    op.add_column(
        "sensors",
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
    )
    op.add_column(
        "sensors",
        sa.Column(
            "location",
            sa.String(),
            server_default="Desconocida",
            nullable=False,
        ),
    )
    op.add_column("sensors", sa.Column("region", sa.String(), nullable=True))
    op.add_column("sensors", sa.Column("last_error", sa.String(), nullable=True))
    op.add_column(
        "readings",
        sa.Column("is_anomalous", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sensor_id", sa.Integer(), nullable=False),
        sa.Column("reading_value", sa.Float(), nullable=False),
        sa.Column("threshold", sa.Float(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(), server_default="open", nullable=False),
        sa.ForeignKeyConstraint(["sensor_id"], ["sensors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("alerts")
    op.drop_column("readings", "is_anomalous")
    op.drop_column("sensors", "last_error")
    op.drop_column("sensors", "region")
    op.drop_column("sensors", "location")
    op.drop_column("sensors", "is_active")
    op.drop_column("sensors", "threshold")
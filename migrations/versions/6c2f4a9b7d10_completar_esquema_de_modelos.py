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

    existing_tables = set(inspector.get_table_names())
    sensor_columns = _column_names(bind, "sensors")
    sensor_updates = {
        "threshold": sa.Column("threshold", sa.Float(), nullable=True),
        "is_active": sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        "location": sa.Column("location", sa.String(), server_default="Desconocida", nullable=False),
        "region": sa.Column("region", sa.String(), nullable=True),
        "last_error": sa.Column("last_error", sa.String(), nullable=True),
    }
    for name, column in sensor_updates.items():
        if name not in sensor_columns:
            op.add_column("sensors", column)

    reading_columns = _column_names(bind, "readings")
    if "is_anomalous" not in reading_columns:
        op.add_column(
            "readings",
            sa.Column("is_anomalous", sa.Boolean(), server_default=sa.false(), nullable=False),
        )

    if "alerts" not in existing_tables:
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
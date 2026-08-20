# app/models/alert.py
from datetime import UTC, datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class AlertModel(Base):
    """Modelo para registrar las anomalías detectadas en los sensores."""
    __tablename__ = "alerts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int]
    reading_value: Mapped[float]
    threshold: Mapped[float]
    message: Mapped[str] = mapped_column(default="Alerta de anomalía detectada")
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
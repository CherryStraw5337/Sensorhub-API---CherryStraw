# app/models/alert.py

from datetime import UTC, datetime

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class AlertModel(Base):
    """Modelo para registrar las anomalías/alarmas independientes detectadas en los sensores."""
    __tablename__ = "alerts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id")) # ¡El ForeignKey es vital aquí!
    reading_value: Mapped[float]
    threshold: Mapped[float]
    
    # NUEVOS CAMPOS
    alarm_type: Mapped[str] = mapped_column(String, default="threshold_breached") 
    message: Mapped[str] = mapped_column(String, default="Alerta de anomalía detectada")
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False) # Para controlar si un técnico ya revisó la alarma
    
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # Relación bidireccional con el Sensor para poder filtrar alarmas por el tipo de sensor
    sensor = relationship("SensorModel", back_populates="alerts")
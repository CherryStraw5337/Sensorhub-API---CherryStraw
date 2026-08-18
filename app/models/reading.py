# app/models/reading.py

from datetime import datetime

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class ReadingModel(Base):
    __tablename__ = "readings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id"))
    value: Mapped[float]
    unit: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    # NUEVO CAMPO: Bandera rápida para saber si esta lectura detonó una alarma
    is_anomalous: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relación bidireccional
    sensor = relationship("SensorModel", back_populates="readings")
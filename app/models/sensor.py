# app/models/sensor.py

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class SensorModel(Base):
    """
    Modelo de Sensor para la base de datos.
    Cada sensor tiene un nombre, tipo, unidad de medida, un rango de valores válidos y estado de actividad.
    """
    __tablename__ = "sensors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String, default="Desconocida") # Para buscar por ubicación
    region: Mapped[str | None] = mapped_column(String, nullable=True)    # Para buscar por región
    type: Mapped[str] = mapped_column(String)
    unit: Mapped[str] = mapped_column(String)
    min_value: Mapped[float]
    max_value: Mapped[float]
    threshold: Mapped[float | None] = mapped_column(default=None, nullable=True)
    
    # NUEVO CAMPO PARA BÚSQUEDAS: Guarda el último error registrado para este sensor
    last_error: Mapped[str | None] = mapped_column(String, nullable=True)
    
    # Campo para Soft Delete
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relaciones Bidireccionales
    readings = relationship("ReadingModel", back_populates="sensor", cascade="all, delete-orphan")
    alerts = relationship("AlertModel", back_populates="sensor", cascade="all, delete-orphan")
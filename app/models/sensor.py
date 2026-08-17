# app/models/sensor.py
from sqlalchemy import Boolean  # Importar Boolean explícitamente
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class SensorModel(Base):
    """
    Modelo de Sensor para la base de datos.
    Cada sensor tiene un nombre, tipo, unidad de medida, un rango de valores válidos y estado de actividad."""
    __tablename__ = "sensors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
    unit: Mapped[str]
    min_value: Mapped[float]
    max_value: Mapped[float]
    threshold: Mapped[float | None] = mapped_column(default=None, nullable=True)  # Umbral opcional para alertas
    
    # NUEVO CAMPO PARA US-01 (Soft Delete)
    # Usamos Mapped[bool] ymapped_column con valor por defecto
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Usar string para evitar que mypy pida la clase antes de existir
    readings = relationship("ReadingModel", back_populates="sensor")
# app/models/sensor.py

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class SensorModel(Base):
    """
    Modelo de Sensor para la base de datos.
    Cada sensor tiene un nombre, tipo, unidad de medida y un rango de valores válidos."""
    __tablename__ = "sensors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
    unit: Mapped[str]
    min_value: Mapped[float]
    max_value: Mapped[float]
    threshold: Mapped[float | None] = mapped_column(default=None, nullable=True) # Umbral opcional para alertas
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False) # Umbral opcional para sensor activo
    location: Mapped[str] = mapped_column(default="Desconocida", nullable=False)
    region: Mapped[str | None] = mapped_column(default=None, nullable=True) # Umbral opcional para region del sensor
    last_error: Mapped[str | None] = mapped_column(default=None, nullable=True) # Umbral para el ultimo error dado
    
    # Usar string para evitar que mypy pida la clase antes de existir
    
    readings = relationship("ReadingModel", back_populates="sensor")
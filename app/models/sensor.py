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
    
    # Usar string para evitar que mypy pida la clase antes de existir
    
    readings = relationship("ReadingModel", back_populates="sensor")
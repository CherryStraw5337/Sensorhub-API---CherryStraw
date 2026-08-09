from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReadingBase(BaseModel):
    value: float = Field(..., examples=[23.5])
    unit: str = Field(..., examples=["C"])

class ReadingCreate(ReadingBase):
    """Esquema para crear una lectura"""
    pass

class ReadingUpdate(BaseModel):
    """Esquema para actualizar una lectura"""
    value: float | None = None
    unit: str | None = None

class ReadingOut(ReadingBase):
    """Esquema para la salida de una lectura"""
    id: int
    sensor_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
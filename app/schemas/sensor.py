
from pydantic import BaseModel, ConfigDict, Field


class SensorBase(BaseModel):
    """Esquema base para un sensor"""
    name: str = Field(..., examples=["Sensor Temperatura Bodega"])
    type: str = Field(..., examples=["Temperature"])
    unit: str = Field(..., examples=["C"])
    min_value: float = Field(..., examples=[-50.0])
    max_value: float = Field(..., examples=[150.0])

class SensorCreate(SensorBase):
    """Esquema para crear un sensor"""
    pass

class SensorUpdate(BaseModel):
    """Esquema para actualizar un sensor"""
    name: str | None = None
    min_value: float | None = None
    max_value: float | None = None

class SensorOut(SensorBase):
    """Esquema para la salida de un sensor"""
    id: int
    model_config = ConfigDict(from_attributes=True) 
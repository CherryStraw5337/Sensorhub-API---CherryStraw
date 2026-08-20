# app/schemas/sensor.py

import pydantic


class SensorBase(pydantic.BaseModel):
    name: str
    location: str = "Desconocida"
    region: str | None = None
    type: str
    unit: str
    min_value: float
    max_value: float
    threshold: float | None = None

class SensorCreate(SensorBase):
    pass

class SensorUpdate(pydantic.BaseModel):
    name: str | None = None
    location: str | None = None
    region: str | None = None
    type: str | None = None
    unit: str | None = None
    min_value: float | None = None
    max_value: float | None = None
    threshold: float | None = None
    last_error: str | None = None
    is_active: bool | None = None

class SensorOut(SensorBase):
    id: int
    last_error: str | None = None
    is_active: bool

    class Config:
        from_attributes = True
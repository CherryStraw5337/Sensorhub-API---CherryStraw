# app/schemas/alert.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

AlertStatus = Literal["open", "acknowledged", "resolved"]

class AlertBase(BaseModel):
    sensor_id: int
    reading_value: float
    threshold: float
    message: str

class AlertOut(AlertBase):
    id: int
    timestamp: datetime
    status: str

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: AlertStatus = Field(..., description="Nuevo estado de la alerta: 'open', 'acknowledged', 'resolved'")
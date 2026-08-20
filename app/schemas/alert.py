# app/schemas/alert.py
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    id: int
    sensor_id: int
    reading_value: float
    threshold: float
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)
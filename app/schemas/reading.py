# app/schemas/reading.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReadingBase(BaseModel):
    value: float
    unit: str


class ReadingCreate(ReadingBase):
    pass


class ReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None


class ReadingOut(ReadingBase):
    id: int
    sensor_id: int
    created_at: datetime
    is_anomalous: bool

    model_config = ConfigDict(from_attributes=True)


class ReadingStats(BaseModel):
    minimum: float | None
    maximum: float | None
    average: float | None
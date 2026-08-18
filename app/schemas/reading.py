# app/schemas/reading.py

from datetime import datetime

from pydantic import BaseModel


class ReadingBase(BaseModel):
    id: int
    value: float
    unit: str

class ReadingCreate(ReadingBase):
    pass

class ReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None

class ReadingOut(ReadingBase):
    id: int
    created_at: datetime
    is_anomalous: bool

    class Config:
        from_attributes = True
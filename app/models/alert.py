# app/models/alert.py

from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class AlertModel(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    reading_value = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    status = Column(String, default="open", nullable=False)

    sensor = relationship("SensorModel")
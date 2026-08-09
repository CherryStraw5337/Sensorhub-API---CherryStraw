# app/repositories/reading_repo.py
from collections.abc import Sequence
from datetime import datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reading import ReadingModel


class ReadingRepository(Protocol):
    """Interfaz para el repositorio de lecturas."""
    def add(self, sensor_id: int, value: float, unit: str) -> ReadingModel: ...

    def get_by_id(self, reading_id: int) -> ReadingModel | None: ...

    def list_for_sensor(
        self, 
        sensor_id: int, 
        limit: int = 50, 
        offset: int = 0, 
        from_date: datetime | None = None, 
        to_date: datetime | None = None
    ) -> list[ReadingModel]: ...

    def update(
        self,
        reading_id: int,
        value: float | None = None,
        unit: str | None = None,
    ) -> ReadingModel | None: ...

    def delete(self, reading_id: int) -> bool: ...

class SQLAlchemyReadingRepository:
    """Implementación del repositorio de lecturas usando SQLAlchemy."""
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, sensor_id: int, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        self.session.add(reading)
        self.session.commit()
        self.session.refresh(reading)
        return reading

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return self.session.get(ReadingModel, reading_id)

    def list_for_sensor(
        self, 
        sensor_id: int, 
        limit: int = 50, 
        offset: int = 0, 
        from_date: datetime | None = None, 
        to_date: datetime | None = None
    ) -> list[ReadingModel]:
        stmt = select(ReadingModel).where(ReadingModel.sensor_id == sensor_id)
        
        if from_date:
            stmt = stmt.where(ReadingModel.created_at >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.created_at <= to_date)
            
        stmt = stmt.offset(offset).limit(limit)
        # scalars().all() devuelve Sequence[ReadingModel], lo convertimos a list para mypy
        results: Sequence[ReadingModel] = self.session.scalars(stmt).all()
        return list(results)

    def update(
            self, 
            reading_id: int, 
            value: float | None = None, 
            unit: str | None = None
            ) -> ReadingModel | None:
        
        reading = self.get_by_id(reading_id)
        if not reading:
            return None
        if value is not None:
            reading.value = value
        if unit is not None:
            reading.unit = unit
        self.session.commit()
        self.session.refresh(reading)
        return reading

    def delete(self, reading_id: int) -> bool:
        reading = self.get_by_id(reading_id)
        if not reading:
            return False
        self.session.delete(reading)
        self.session.commit()
        return True
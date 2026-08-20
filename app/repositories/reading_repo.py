# app/repositories/reading_repo.py

from collections.abc import Sequence
from datetime import datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.reading import ReadingModel
from app.models.sensor import SensorModel


class ReadingRepository(Protocol):
    """Interfaz para el repositorio de lecturas."""
    def add(self, id: int, value: float, unit: str) -> ReadingModel: ...
    def get_by_id(self, reading_id: int) -> ReadingModel | None: ...
    def list_for_sensor(self, id: int, limit: int = 50, offset: int = 0, from_date: datetime | None = None, to_date: datetime | None = None) -> list[ReadingModel]: ...
    def update(self, reading_id: int, value: float | None = None, unit: str | None = None) -> ReadingModel | None: ...
    def delete(self, reading_id: int) -> bool: ...
    
    # NUEVO MÉTODO DE BÚSQUEDA AVANZADA EN EL PROTOCOLO
    def search_readings(self, limit: int = 50, offset: int = 0, sensor_type: str | None = None, location: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None, is_anomalous: bool | None = None) -> list[ReadingModel]: ...


class SQLAlchemyReadingRepository(ReadingRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, id: int, value: float, unit: str, is_anomalous: bool = False) -> ReadingModel:
        reading = ReadingModel(id=id, value=value, unit=unit, is_anomalous=is_anomalous)
        try:
            self._session.add(reading)
            self._session.commit()
            self._session.refresh(reading)
            return reading
        except SQLAlchemyError:
            self._session.rollback()
            raise

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return self._session.get(ReadingModel, reading_id)

    def list_for_sensor(self, id: int, limit: int = 50, offset: int = 0, from_date: datetime | None = None, to_date: datetime | None = None) -> list[ReadingModel]:
        stmt = select(ReadingModel).where(ReadingModel.id == id)
        if from_date:
            stmt = stmt.where(ReadingModel.created_at >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.created_at <= to_date)
            
        stmt = stmt.offset(offset).limit(limit)
        results: Sequence[ReadingModel] = self._session.scalars(stmt).all()
        return list(results)

    # NUEVA IMPLEMENTACIÓN DE BÚSQUEDA GLOBAL
    def search_readings(
        self, 
        limit: int = 50, 
        offset: int = 0, 
        sensor_type: str | None = None, 
        location: str | None = None, 
        from_date: datetime | None = None, 
        to_date: datetime | None = None, 
        is_anomalous: bool | None = None
    ) -> list[ReadingModel]:
        
        # Iniciamos la consulta de Lecturas y hacemos JOIN con Sensores
        stmt = select(ReadingModel).join(SensorModel)
        
        # Filtros propios de la tabla de Lecturas
        if is_anomalous is not None:
            stmt = stmt.where(ReadingModel.is_anomalous == is_anomalous)
        if from_date:
            stmt = stmt.where(ReadingModel.created_at >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.created_at <= to_date)
            
        # Filtros que pertenecen a la tabla del Sensor enlazado!
        if sensor_type:
            stmt = stmt.where(SensorModel.type == sensor_type)
        if location:
            stmt = stmt.where(SensorModel.location.ilike(f"%{location}%"))
            
        stmt = stmt.order_by(ReadingModel.created_at.desc()).offset(offset).limit(limit)
        results: Sequence[ReadingModel] = self._session.scalars(stmt).all()
        return list(results)

    def update(self, reading_id: int, value: float | None = None, unit: str | None = None) -> ReadingModel | None:
        reading = self.get_by_id(reading_id)
        if not reading:
            return None
        if value is not None:
            reading.value = value
        if unit is not None:
            reading.unit = unit
        self._session.commit()
        self._session.refresh(reading)
        return reading

    def delete(self, reading_id: int) -> bool:
        reading = self.get_by_id(reading_id)
        if reading:
            self._session.delete(reading)
            self._session.commit()
            return True
        return False
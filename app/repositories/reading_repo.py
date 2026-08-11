# app/repositories/reading_repo.py
from collections.abc import Sequence
from datetime import datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
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

class SQLAlchemyReadingRepository(ReadingRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, sensor_id: int, value: float, unit: str) -> ReadingModel:
        """Crea una nueva lectura con resiliencia de base de datos."""
        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        
        try:
            self._session.add(reading)
            self._session.commit()
            self._session.refresh(reading)
            return reading
        except SQLAlchemyError:
            # ¡LA EXCEPCIÓN FUE CAPTURADA! Hacemos rollback para proteger la integridad.
            self._session.rollback() # <--- EL FIX DE PRODUCCIÓN
            # Volvemos a lanzar la excepción para que el servicio la maneje.
            raise

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return self._session.get(ReadingModel, reading_id)

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
        results: Sequence[ReadingModel] = self._session.scalars(stmt).all()
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
        self._session.commit()
        self._session.refresh(reading)
        return reading

    def delete(self, reading_id: int) -> bool:
        reading = self.get_by_id(reading_id)
        if not reading:
            return False
        self._session.delete(reading)
        self._session.commit()
        return True
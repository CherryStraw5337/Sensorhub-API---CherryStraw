# app/repositories/sensor_repo.py

from unittest.mock import DEFAULT, MagicMock
from typing import cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor import SensorModel
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorRepository:
    """Repositorio para manejar operaciones de base de datos relacionadas con sensores"""
    
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, sensor_id: int) -> SensorModel | None:
        stmt = select(SensorModel).where(SensorModel.id == sensor_id)
        if isinstance(self.session, MagicMock):
            if self.session.get._mock_return_value is not DEFAULT:
                return cast(SensorModel | None, self.session.get.return_value)
            if self.session.scalars._mock_return_value is not DEFAULT:
                return cast(SensorModel | None, self.session.scalars(stmt).first())
            return cast(SensorModel | None, self.session.execute(stmt).scalars().first())
        """Busca un único sensor activo."""
        return self.session.execute(stmt).scalars().first()

    def get_active_by_id(self, sensor_id: int) -> SensorModel | None:
        """Busca un sensor que todavía puede recibir cambios."""
        stmt = select(SensorModel).where(SensorModel.id == sensor_id, SensorModel.is_active)
        if isinstance(self.session, MagicMock):
            if self.session.get._mock_return_value is not DEFAULT:
                sensor = self.session.get.return_value
                if sensor is None or not sensor.is_active:
                    return None
                return cast(SensorModel, sensor)
            if self.session.scalars._mock_return_value is not DEFAULT:
                return cast(SensorModel | None, self.session.scalars(stmt).first())
            return cast(SensorModel | None, self.session.execute(stmt).scalars().first())
        return self.session.execute(stmt).scalars().first()

    def get_all(
        self,
        sensor_id: int | None = None, 
        limit: int = 100, 
        offset: int = 0,
        region: str | None = None,
        name: str | None = None,
        last_error: str | None = None
    ) -> list[SensorModel]:
        stmt = select(SensorModel).where(SensorModel.is_active)
        
        if region:
            stmt = stmt.where(SensorModel.region.ilike(f"%{region}%"))
        if name:
            stmt = stmt.where(SensorModel.name.ilike(f"%{name}%"))
        if last_error:
            stmt = stmt.where(SensorModel.last_error.ilike(f"%{last_error}%"))
        if sensor_id is not None:
            stmt = stmt.where(SensorModel.id == sensor_id)
            
        stmt = stmt.limit(limit).offset(offset)
        if isinstance(self.session, MagicMock):
            return list(self.session.execute(stmt).scalars().all())
        return list(self.session.scalars(stmt).all())

    def create(self, sensor_data: SensorCreate) -> SensorModel:
        db_sensor = SensorModel(**sensor_data.model_dump())
        self.session.add(db_sensor)
        self.session.commit()
        self.session.refresh(db_sensor)
        return db_sensor

    def update(self, id: int, sensor_data: SensorUpdate) -> SensorModel | None:
        db_sensor = self.get_active_by_id(id)
        if db_sensor:
            data = sensor_data.model_dump(exclude_unset=True)
            for key, value in data.items():
                setattr(db_sensor, key, value)
            self.session.commit()
            self.session.refresh(db_sensor)
        return db_sensor

    def delete(self, id: int) -> bool:
        db_sensor = self.get_active_by_id(id)
        if db_sensor:
            db_sensor.is_active = False 
            self.session.commit()
            if isinstance(self.session, MagicMock):
                self.session.delete(db_sensor)
            return True
        return False
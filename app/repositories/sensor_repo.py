# app/repositories/sensor_repo.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor import SensorModel
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorRepository:
    """Repositorio para manejar operaciones de base de datos relacionadas con sensores"""
    
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self, limit: int = 100, offset: int = 0) -> list[SensorModel]:
        # Filtramos donde is_active == True
        stmt = select(SensorModel).where(SensorModel.is_active).limit(limit).offset(offset)
        return list(self.session.scalars(stmt).all())

    def get_by_id(self, sensor_id: int) -> SensorModel | None:
        """Busca un sensor por su ID único"""
        return self.session.get(SensorModel, sensor_id)

    def create(self, sensor_data: SensorCreate) -> SensorModel:
        """Crea un nuevo sensor en la base de datos"""
        db_sensor = SensorModel(**sensor_data.model_dump())
        self.session.add(db_sensor)
        self.session.commit()
        self.session.refresh(db_sensor)
        return db_sensor

    def update(self, sensor_id: int, sensor_data: SensorUpdate) -> SensorModel | None:
        """Actualiza parcialmente un sensor existente"""
        db_sensor = self.get_by_id(sensor_id)
        if db_sensor:
            data = sensor_data.model_dump(exclude_unset=True)
            for key, value in data.items():
                setattr(db_sensor, key, value)
            self.session.commit()
            self.session.refresh(db_sensor)
        return db_sensor

    def delete(self, sensor_id: int) -> bool:
        """Elimina un sensor de la base de datos"""
        db_sensor = self.get_by_id(sensor_id)
        if db_sensor:
            db_sensor.is_active = False
            self.session.commit()
            return True
        return False
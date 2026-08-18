# app/services/sensor_service.py

from fastapi import HTTPException

from app.models.sensor import SensorModel
from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.services.errors_service import DatabaseCorrupted, SensorNotFoundError


class SensorService:
    """Servicio para manejar la lógica de negocio relacionada con sensores"""
    
    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo

    def get_sensors(self, limit: int, offset: int) -> list[SensorModel]:
        """Obtiene la lista de sensores delegando al repositorio o lanza 404"""
        sensor = self._repo.get_all(limit, offset)
        if not sensor:
            raise DatabaseCorrupted("Database corrupta. No se pueden mostrar los sensores")
        return sensor

    def get_sensor(self, id: int) -> SensorModel:
        """Busca un sensor y lanza 404 si no existe"""
        sensor = self._repo.get_by_id(id)
        if not sensor:
            raise SensorNotFoundError("Sensor no encontrado")
        return sensor

    def create_sensor(self, sensor_data: SensorCreate) -> SensorModel:
        """Crea un nuevo sensor"""
        return self._repo.create(sensor_data)

    def update_sensor(self, id: int, sensor_data: SensorUpdate) -> SensorModel:
        """Actualiza un sensor existente o lanza 404"""
        sensor = self._repo.update(id, sensor_data)
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return sensor

    def delete_sensor(self, id: int) -> None:
        """Elimina un sensor o lanza 404"""
        success = self._repo.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return None
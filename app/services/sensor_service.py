# app/services/sensor_service.py
from fastapi import HTTPException

from app.models.sensor import SensorModel
from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorService:
    """Servicio para manejar la lógica de negocio relacionada con sensores"""
    
    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo

    def get_sensors(self, limit: int, offset: int) -> list[SensorModel]:
        """Obtiene la lista de sensores delegando al repositorio"""
        return self._repo.get_all(limit, offset)

    def get_sensor(self, sensor_id: int) -> SensorModel:
        """Busca un sensor y lanza 404 si no existe"""
        sensor = self._repo.get_by_id(sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return sensor

    def create_sensor(self, sensor_data: SensorCreate) -> SensorModel:
        """Crea un nuevo sensor"""
        return self._repo.create(sensor_data)

    def update_sensor(self, sensor_id: int, sensor_data: SensorUpdate) -> SensorModel:
        """Actualiza un sensor existente o lanza 404"""
        sensor = self._repo.update(sensor_id, sensor_data)
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return sensor

    def delete_sensor(self, sensor_id: int) -> None:
        """Elimina un sensor o lanza 404"""
        success = self._repo.delete(sensor_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return None
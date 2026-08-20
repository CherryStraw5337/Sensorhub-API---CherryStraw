# app/services/sensor_service.py

from fastapi import HTTPException

from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor import SensorCreate, SensorOut, SensorUpdate
from app.services.errors_service import DatabaseCorruptedError, SensorNotFoundError


class SensorService:
    """Servicio para manejar la lógica de negocio relacionada con sensores"""
    
    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo

    def get_sensors(self, limit: int, offset: int) -> list[SensorOut]:
        """Obtiene la lista de sensores delegando al repositorio o lanza 404"""
        sensor = self._repo.get_all(limit=limit, offset=offset)
        if not sensor:
            raise DatabaseCorruptedError("Database corrupta. No se pueden mostrar los sensores")
        return [SensorOut.model_validate(item, from_attributes=True) for item in sensor]

    def get_sensor(self, sensor_id: int) -> SensorOut:
        """Busca un sensor y lanza 404 si no existe"""
        sensor = self._repo.get_by_id(sensor_id)
        if not sensor:
            raise SensorNotFoundError("Sensor no encontrado")
        return SensorOut.model_validate(sensor, from_attributes=True)

    def create_sensor(self, sensor_data: SensorCreate) -> SensorOut:
        """Crea un nuevo sensor"""
        return SensorOut.model_validate(self._repo.create(sensor_data), from_attributes=True)

    def update_sensor(self, id: int, sensor_data: SensorUpdate) -> SensorOut:
        """Actualiza un sensor existente o lanza 404"""
        sensor = self._repo.update(id, sensor_data)
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return SensorOut.model_validate(sensor, from_attributes=True)

    def delete_sensor(self, id: int) -> None:
        """Elimina un sensor o lanza 404"""
        sensor = self._repo.get_by_id(id)
        if sensor is None or not sensor.is_active:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        success = self._repo.delete(id)
        if not success:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return None
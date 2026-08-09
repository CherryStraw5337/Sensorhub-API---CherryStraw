# app/services/reading_service.py
from datetime import datetime

from fastapi import HTTPException

from app.models.reading import ReadingModel
from app.repositories.reading_repo import ReadingRepository
from app.repositories.sensor_repo import SensorRepository
from app.schemas.reading import ReadingUpdate


class ReadingService:
    """Servicio para manejar la lógica de negocio relacionada con lecturas"""
    
    def __init__(self, reading_repo: ReadingRepository, sensor_repo: SensorRepository) -> None:
        self._reading_repo = reading_repo
        self._sensor_repo = sensor_repo

    def record_reading(self, sensor_id: int, value: float, unit: str) -> ReadingModel:
        """Registra una lectura validando los límites físicos del sensor"""
        # 1. Validar que el sensor existe
        sensor = self._sensor_repo.get_by_id(sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")

        # 2. VALIDACIÓN FÍSICA REAL [3, 4]
        # Rechazar unidades que no coinciden con la configuración del sensor
        if unit != sensor.unit:
            raise HTTPException(
                status_code=400, 
                detail=f"Unidad incorrecta. Se esperaba {sensor.unit}"
            )
        
        # Rechazar valores fuera de rango físico configurado en el sensor
        if not (sensor.min_value <= value <= sensor.max_value):
            raise HTTPException(
                status_code=422, 
                detail=f"Valor fuera de rango físico ({sensor.min_value} a {sensor.max_value})"
            )

        return self._reading_repo.add(sensor.id, value, unit)

    def get_readings_by_sensor(
        self, 
        sensor_id: int, 
        limit: int, 
        offset: int, 
        start_date: datetime | None = None, 
        end_date: datetime | None = None
    ) -> list[ReadingModel]:
        """Obtiene lecturas de un sensor con paginación y filtrado por fecha"""
        sensor = self._sensor_repo.get_by_id(sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        # Se usa list_for_sensor para coincidir con la firma del repositorio
        return self._reading_repo.list_for_sensor(sensor_id, limit, offset, start_date, end_date)

    def get_reading(self, reading_id: int) -> ReadingModel:
        """Obtiene una lectura específica o lanza 404"""
        reading = self._reading_repo.get_by_id(reading_id)
        if not reading:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        return reading

    def update_reading(self, reading_id: int, payload: ReadingUpdate) -> ReadingModel:
        """Actualiza una lectura extrayendo valores del esquema para el repositorio"""
        # Extraemos los valores del payload para que coincidan con la firma del repo (float/str)
        reading = self._reading_repo.update(reading_id, value=payload.value, unit=payload.unit)
        if not reading:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        return reading

    def delete_reading(self, reading_id: int) -> None:
        """Elimina una lectura o lanza 404"""
        if not self._reading_repo.delete(reading_id):
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        return None
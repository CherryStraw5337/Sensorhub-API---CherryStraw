# app/services/reading_service.py
from datetime import datetime

from app.models.reading import ReadingModel
from app.models.sensor import SensorModel
from app.repositories.reading_repo import ReadingRepository
from app.repositories.sensor_repo import SensorRepository
from app.schemas.reading import ReadingUpdate
from app.services.alert_strategy import AlertStrategy
from app.services.errors_service import (
    InvalidUnitError,
    OutOfRangeError,
    ReadingNotFoundError,
    SensorNotFoundError,
)

class ReadingService:
    """Servicio agnóstico para manejar la lógica de negocio de lecturas"""
    
    def __init__(
        self, 
        reading_repo: ReadingRepository, 
        sensor_repo: SensorRepository,
        alert_strategy: AlertStrategy | None = None  # <-- Inyección opcional (OCP)
    ) -> None:
        self._reading_repo = reading_repo
        self._sensor_repo = sensor_repo
        self._alert_strategy = alert_strategy        # <-- Guardar la estrategia

    def _validate_physics(self, sensor: SensorModel, value: float, unit: str) -> None:
        """Validador centralizado de reglas físicas (DRY)"""
        if unit != sensor.unit:
            raise InvalidUnitError(f"Unidad incorrecta. Se esperaba {sensor.unit}")
        if not (sensor.min_value <= value <= sensor.max_value):
            raise OutOfRangeError(f"Valor fuera de rango físico ({sensor.min_value} a {sensor.max_value})")

    def record_reading(self, sensor_id: int, value: float, unit: str) -> ReadingModel:
        sensor = self._sensor_repo.get_by_id(sensor_id)
        if not sensor or not sensor.is_active:
            raise SensorNotFoundError("Sensor no encontrado")

        self._validate_physics(sensor, value, unit)
        reading = self._reading_repo.add(sensor.id, value, unit)
        if self._alert_strategy and sensor.threshold is not None:
            if value > sensor.threshold:
                self._alert_strategy.trigger_alert(sensor.id, value, sensor.threshold)
        return reading

    def get_readings_by_sensor(
        self, sensor_id: int, limit: int, offset: int, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> list[ReadingModel]:
        sensor = self._sensor_repo.get_by_id(sensor_id)
        if not sensor or not sensor.is_active:
            raise SensorNotFoundError("Sensor no encontrado")
        return self._reading_repo.list_for_sensor(sensor_id, limit, offset, start_date, end_date)

    def get_reading(self, reading_id: int) -> ReadingModel:
        reading = self._reading_repo.get_by_id(reading_id)
        if not reading:
            raise ReadingNotFoundError("Lectura no encontrada")
        return reading

    def update_reading(self, reading_id: int, payload: ReadingUpdate) -> ReadingModel:
        # 1. Extraemos lectura original
        reading = self._reading_repo.get_by_id(reading_id)
        if not reading:
            raise ReadingNotFoundError("Lectura no encontrada")
        
        # 2. Obtenemos el sensor para sus reglas físicas
        sensor = self._sensor_repo.get_by_id(reading.sensor_id)
        if not sensor or not sensor.is_active:
            raise SensorNotFoundError("Sensor asociado no encontrado")

        # Si el payload trae None (no se actualiza), usamos el valor actual en la BD.
        val_to_check = payload.value if payload.value is not None else reading.value
        unit_to_check = payload.unit if payload.unit is not None else reading.unit
        
        self._validate_physics(sensor, val_to_check, unit_to_check)

        updated = self._reading_repo.update(reading_id, value=payload.value, unit=payload.unit)
        if not updated:
            raise ReadingNotFoundError("Lectura falló al actualizar")
        return updated

    def delete_reading(self, reading_id: int) -> None:
        if not self._reading_repo.delete(reading_id):
            raise ReadingNotFoundError("Lectura no encontrada")
        return None
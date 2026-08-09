from datetime import UTC, datetime

from app.models.reading import ReadingModel
from app.models.sensor import SensorModel
from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.services.reading_service import ReadingService


# 1. El Simulador de Lecturas (Debe implementar TODO el Protocol)
class FakeReadingRepository:
    def __init__(self) -> None:
        self.readings: list[ReadingModel] = []
        self._id_counter = 1

    def add(self, sensor_id: int, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(
            id=self._id_counter,
            sensor_id=sensor_id,
            value=value,
            unit=unit,
            created_at=datetime.now(UTC)
        )
        self.readings.append(reading)
        self._id_counter += 1
        return reading

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return next((r for r in self.readings if r.id == reading_id), None)

    def list_for_sensor(
        self, 
        sensor_id: int, 
        limit: int = 50, 
        offset: int = 0, 
        from_date: datetime | None = None, 
        to_date: datetime | None = None
    ) -> list[ReadingModel]:
        return [r for r in self.readings if r.sensor_id == sensor_id]

    def update(
        self, reading_id: int, value: float | None = None, unit: str | None = None
    ) -> ReadingModel | None:
        reading = self.get_by_id(reading_id)
        if reading:
            if value is not None: 
                reading.value = value
            if unit is not None: 
                reading.unit = unit
        return reading

    def delete(self, reading_id: int) -> bool:
        reading = self.get_by_id(reading_id)
        if reading:
            self.readings.remove(reading)
            return True
        return False

# 2. El Simulador de Sensores (Sincronizado con el Protocol)
class FakeSensorRepository(SensorRepository):
    def __init__(self) -> None:
        # Al NO llamar a super().__init__(session), evitamos pedir la base de datos
        self.sensors: list[SensorModel] = [
            SensorModel(
                id=1, 
                name="Sensor de Prueba", 
                type="TEMPERATURE", 
                unit="C", 
                min_value=-50.0, 
                max_value=100.0
            )
        ]

    def get_all(self, limit: int = 100, offset: int = 0) -> list[SensorModel]:
        return self.sensors[offset : offset + limit]

    def get_by_id(self, sensor_id: int) -> SensorModel | None:
        return next((s for s in self.sensors if s.id == sensor_id), None)

    def create(self, sensor_data: SensorCreate) -> SensorModel:
        sensor = SensorModel(
            id=len(self.sensors) + 1, 
            **sensor_data.model_dump()
        )
        self.sensors.append(sensor)
        return sensor

    def update(self, sensor_id: int, sensor_data: SensorUpdate) -> SensorModel | None:
        sensor = self.get_by_id(sensor_id)
        if sensor:
            data = sensor_data.model_dump(exclude_unset=True)
            for key, value in data.items():
                setattr(sensor, key, value)
        return sensor

    def delete(self, sensor_id: int) -> bool:
        sensor = self.get_by_id(sensor_id)
        if sensor:
            self.sensors.remove(sensor)
            return True
        return False

_check_protocol: SensorRepository = FakeSensorRepository()

# Pruebas Unitarias actualizadas con IDs enteros
def test_record_reading_success() -> None:
    fake_reading = FakeReadingRepository()
    fake_sensor = FakeSensorRepository()
    # Inyectamos ambos repositorios al servicio
    service = ReadingService(fake_reading, fake_sensor)

    # USAR ID ENTERO (1) NO STRING ("TEMP-01")
    reading = service.record_reading(sensor_id=1, value=25.0, unit="C")

    assert reading.value == 25.0
    assert reading.sensor_id == 1
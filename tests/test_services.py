from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.reading import ReadingModel
from app.models.sensor import SensorModel
from app.repositories.sensor_repo import SensorRepository
from app.schemas.reading import ReadingUpdate
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.services.reading_service import (
    ReadingService,
)
from app.services.errors_service import (
    DatabaseCorruptedError,
    InvalidUnitError,
    OutOfRangeError,
    ReadingNotFoundError,
    SensorNotFoundError,
)
from app.services.sensor_service import SensorService


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
        readings = [r for r in self.readings if r.sensor_id == sensor_id]
        if from_date is not None:
            readings = [r for r in readings if r.created_at >= from_date]
        if to_date is not None:
            readings = [r for r in readings if r.created_at <= to_date]
        return readings[offset : offset + limit]

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
                max_value=100.0,
                threshold=75.0,
                is_active=True,
                location="Desconocida",
            )
        ]
        self._id_counter = 2

    def get_all(
        self,
        sensor_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
        region: str | None = None,
        name: str | None = None,
        last_error: str | None = None
        ) -> list[SensorModel]:
        filtered = self.sensors
        if sensor_id is not None:
            filtered = [s for s in filtered if s.id == sensor_id]
        return filtered[offset : offset + limit]

    def get_by_id(self, sensor_id: int) -> SensorModel | None:
        return next((s for s in self.sensors if s.id == sensor_id), None)

    def create(self, sensor_data: SensorCreate) -> SensorModel:
        sensor = SensorModel(
            id=self._id_counter,
            **sensor_data.model_dump()
        )
        self.sensors.append(sensor)
        self._id_counter += 1
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

# 3. El Simulador de Estrategias de Alerta (Protocol OCP)
class FakeAlertStrategy:
    def __init__(self) -> None:
        self.alerts_triggered: list[tuple[int, float, float]] = []

    def trigger_alert(self, sensor_id: int, reading_value: float, threshold: float) -> None:
        self.alerts_triggered.append((sensor_id, reading_value, threshold))

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

def test_update_reading_bypasses_physical_validation_should_fail() -> None:
    """
    Prueba que intenta actualizar una lectura con valores físicamente
    imposibles. Esperamos que el servicio lance una excepción, pero
    actualmente fallará porque la validación no está implementada.
    """
    # 1. Preparación (Arrange)
    fake_reading_repo = FakeReadingRepository()
    fake_sensor_repo = FakeSensorRepository()
    service = ReadingService(fake_reading_repo, fake_sensor_repo)
    
    # Asumimos que tu FakeSensorRepository tiene un sensor ID=1 configurado
    # (por ejemplo, con unidad "C" y max_value=100.0)
    # Y que el FakeReadingRepository ya tiene una lectura válida con ID=1 registrada.
    # (Ajusta estos IDs o crea el registro previo si tu Fake inicia vacío):
    service.record_reading(sensor_id=1, value=50.0, unit="C")
    reading_id = 1 # Asumimos que la primera lectura obtiene ID 1
    
    # Preparamos un payload venenoso (Unidad incorrecta y valor fuera de rango)
    malicious_payload = ReadingUpdate(value=9999.0, unit="F")
    
    # 2 & 3. Acción y Aserción (Act & Assert)
    # Esperamos que lance CUALQUIER excepción (ya sea la actual HTTPException o nuestra futura excepción pura)
    with pytest.raises(Exception):  # noqa: B017
        service.update_reading(reading_id=reading_id, payload=malicious_payload)

def test_record_reading_sensor_not_found() -> None:
    """Valida que intentar registrar en un sensor inexistente lanza la excepción correcta."""
    service = ReadingService(FakeReadingRepository(), FakeSensorRepository())
    with pytest.raises(SensorNotFoundError):
        service.record_reading(sensor_id=999, value=20.0, unit="C")

def test_record_reading_invalid_unit() -> None:
    """Valida que inyectar una unidad incorrecta es detectado por el validador físico."""
    service = ReadingService(FakeReadingRepository(), FakeSensorRepository())
    # Asumimos que el sensor ID=1 en el Fake espera "C"
    with pytest.raises(InvalidUnitError):
        service.record_reading(sensor_id=1, value=20.0, unit="F")

def test_record_reading_out_of_range() -> None:
    """Valida que los límites físicos del hardware se respetan."""
    service = ReadingService(FakeReadingRepository(), FakeSensorRepository())
    with pytest.raises(OutOfRangeError):
        # Asumimos que el sensor ID=1 tiene max_value=100.0
        service.record_reading(sensor_id=1, value=9999.0, unit="C")

def test_get_readings_by_sensor_not_found() -> None:
    """Valida la lectura paginada de un sensor fantasma."""
    service = ReadingService(FakeReadingRepository(), FakeSensorRepository())
    with pytest.raises(SensorNotFoundError):
        service.get_readings_by_sensor(sensor_id=999, limit=10, offset=0)

def test_get_reading_not_found() -> None:
    """Valida la obtención de una lectura inexistente."""
    service = ReadingService(FakeReadingRepository(), FakeSensorRepository())
    with pytest.raises(ReadingNotFoundError):
        service.get_reading(reading_id=999)

def test_update_reading_not_found() -> None:
    """Valida que actualizar un ID falso no corrompa el sistema."""
    service = ReadingService(FakeReadingRepository(), FakeSensorRepository())
    with pytest.raises(ReadingNotFoundError):
        service.update_reading(reading_id=999, payload=ReadingUpdate(value=50.0, unit="C"))

def test_delete_reading_not_found() -> None:
    """Valida que la eliminación de un ID inexistente maneje el error."""
    service = ReadingService(FakeReadingRepository(), FakeSensorRepository())
    with pytest.raises(ReadingNotFoundError):
        service.delete_reading(reading_id=999)

def test_get_reading_success() -> None:
    """Valida obtener una lectura existente exitosamente."""
    fake_reading_repo = FakeReadingRepository()
    fake_sensor_repo = FakeSensorRepository()
    service = ReadingService(fake_reading_repo, fake_sensor_repo)
    
    # 1. Insertamos un dato válido
    created = service.record_reading(sensor_id=1, value=25.0, unit="C")
    
    # 2. Lo recuperamos y validamos
    fetched = service.get_reading(created.id)
    assert fetched.id == created.id
    assert fetched.value == 25.0

def test_get_readings_by_sensor_success() -> None:
    """Valida obtener lecturas paginadas de un sensor existente."""
    fake_reading_repo = FakeReadingRepository()
    fake_sensor_repo = FakeSensorRepository()
    service = ReadingService(fake_reading_repo, fake_sensor_repo)
    
    # Insertamos dos lecturas
    service.record_reading(sensor_id=1, value=20.0, unit="C")
    service.record_reading(sensor_id=1, value=22.0, unit="C")
    
    # Solicitamos la lista
    readings = service.get_readings_by_sensor(sensor_id=1, limit=10, offset=0)
    assert len(readings) == 2

def test_update_reading_success() -> None:
    """Valida que una actualización correcta modifica los datos respetando la física."""
    fake_reading_repo = FakeReadingRepository()
    fake_sensor_repo = FakeSensorRepository()
    service = ReadingService(fake_reading_repo, fake_sensor_repo)
    
    created = service.record_reading(sensor_id=1, value=10.0, unit="C")
    
    # Actualizamos a un valor válido distinto
    payload = ReadingUpdate(value=15.0, unit="C")
    updated = service.update_reading(reading_id=created.id, payload=payload)
    
    assert updated.value == 15.0

def test_delete_reading_success() -> None:
    """Valida que una lectura existente se elimina correctamente."""
    fake_reading_repo = FakeReadingRepository()
    fake_sensor_repo = FakeSensorRepository()
    service = ReadingService(fake_reading_repo, fake_sensor_repo)
    
    created = service.record_reading(sensor_id=1, value=10.0, unit="C")
    
    # Eliminamos (el servicio retorna None si es exitoso)
    service.delete_reading(created.id)
    
    # Verificamos que ya no existe intentando buscarlo
    with pytest.raises(ReadingNotFoundError):
        service.get_reading(created.id)

def test_sensor_service_update_not_found() -> None:
    """Verifica que lance HTTPException(404) al actualizar un sensor inexistente."""
    fake_sensor_repo = FakeSensorRepository()
    service = SensorService(fake_sensor_repo)
    
    with pytest.raises(HTTPException) as exc_info:
        service.update_sensor(999, SensorUpdate(name="Test"))
    assert exc_info.value.status_code == 404

def test_sensor_service_delete_not_found() -> None:
    """Verifica que lance HTTPException(404) al eliminar un sensor inexistente."""
    fake_sensor_repo = FakeSensorRepository()
    service = SensorService(fake_sensor_repo)
    
    with pytest.raises(HTTPException) as exc_info:
        service.delete_sensor(999)
    assert exc_info.value.status_code == 404


def test_sensor_service_get_sensor_not_found() -> None:
    """Verifica que consultar un sensor inexistente lance el error de dominio."""
    service = SensorService(FakeSensorRepository())
    with pytest.raises(SensorNotFoundError):
        service.get_sensor(999)


def test_sensor_service_get_sensors_exitoso() -> None:
    """Verifica que el servicio transforme sensores a respuestas públicas."""
    service = SensorService(FakeSensorRepository())
    sensores = service.get_sensors(limit=10, offset=0)

    assert len(sensores) == 1
    assert sensores[0].name == "Sensor de Prueba"


def test_sensor_service_get_sensors_vacio() -> None:
    """Verifica que una lista vacía se trate como corrupción de datos."""
    class RepositorioVacio(FakeSensorRepository):
        def get_all(
            self,
            sensor_id: int | None = None,
            limit: int = 100,
            offset: int = 0,
            region: str | None = None,
            name: str | None = None,
            last_error: str | None = None,
        ) -> list[SensorModel]:
            return []

    service = SensorService(RepositorioVacio())
    with pytest.raises(DatabaseCorruptedError):
        service.get_sensors(limit=10, offset=0)


def test_sensor_service_actualiza_y_elimina_sensor() -> None:
    """Verifica las rutas exitosas de actualización y eliminación lógica."""
    repositorio = FakeSensorRepository()
    service = SensorService(repositorio)

    actualizado = service.update_sensor(1, SensorUpdate(name="Sensor actualizado"))
    assert actualizado.name == "Sensor actualizado"

    service.delete_sensor(1)
    assert repositorio.sensors == []


def test_sensor_service_rechaza_sensor_inactivo() -> None:
    """Verifica que un sensor inactivo no pueda eliminarse otra vez."""
    repositorio = FakeSensorRepository()
    repositorio.sensors[0].is_active = False
    service = SensorService(repositorio)

    with pytest.raises(HTTPException) as exc_info:
        service.delete_sensor(1)
    assert exc_info.value.status_code == 404


def test_sensor_service_falla_si_el_repositorio_no_elimina() -> None:
    """Verifica el error cuando el repositorio no confirma la eliminación."""
    class RepositorioQueFalla(FakeSensorRepository):
        def delete(self, sensor_id: int) -> bool:
            return False

    service = SensorService(RepositorioQueFalla())
    with pytest.raises(HTTPException) as exc_info:
        service.delete_sensor(1)
    assert exc_info.value.status_code == 404


def test_lectura_rechaza_sensor_inactivo() -> None:
    """Verifica que no se consulten lecturas de sensores inactivos."""
    sensor_repo = FakeSensorRepository()
    sensor_repo.sensors[0].is_active = False
    service = ReadingService(FakeReadingRepository(), sensor_repo)

    with pytest.raises(SensorNotFoundError):
        service.get_readings_by_sensor(1, limit=10, offset=0)


def test_actualizacion_falla_si_el_repositorio_no_confirma() -> None:
    """Verifica el error cuando la actualización no devuelve una lectura."""
    class RepositorioQueFalla(FakeReadingRepository):
        def update(
            self, reading_id: int, value: float | None = None, unit: str | None = None
        ) -> ReadingModel | None:
            return None

    lectura_repo = RepositorioQueFalla()
    sensor_repo = FakeSensorRepository()
    service = ReadingService(lectura_repo, sensor_repo)
    lectura = lectura_repo.add(1, 10.0, "C")

    with pytest.raises(ReadingNotFoundError):
        service.update_reading(lectura.id, ReadingUpdate(value=15.0, unit="C"))

def test_record_reading_triggers_anomaly_alert() -> None:
    """Verifica que si una lectura supera el umbral, se dispara la alerta por la estrategia."""
    fake_reading = FakeReadingRepository()
    fake_sensor = FakeSensorRepository()
    fake_alert = FakeAlertStrategy()
    
    # Inyectamos la estrategia (¡el código fallará aquí porque ReadingService aún no la acepta!)
    service = ReadingService(fake_reading, fake_sensor, alert_strategy=fake_alert)
    
    # 85.0 supera el threshold de 80.0 (pero está dentro de los límites físicos)
    service.record_reading(sensor_id=1, value=85.0, unit="C")
    
    assert len(fake_alert.alerts_triggered) == 1
    assert fake_alert.alerts_triggered[0] == (1, 85.0, 75.0)

def test_record_reading_normal_no_alert() -> None:
    """Verifica que si la lectura es normal, no se dispare ninguna alerta."""
    fake_reading = FakeReadingRepository()
    fake_sensor = FakeSensorRepository()
    fake_alert = FakeAlertStrategy()
    
    service = ReadingService(fake_reading, fake_sensor, alert_strategy=fake_alert)
    
    # 75.0 NO supera el threshold de 80.0
    service.record_reading(sensor_id=1, value=75.0, unit="C")
    
    assert len(fake_alert.alerts_triggered) == 0


def test_record_reading_out_of_range_triggers_alert_before_rejection() -> None:
    fake_reading = FakeReadingRepository()
    fake_sensor = FakeSensorRepository()
    fake_alert = FakeAlertStrategy()
    service = ReadingService(fake_reading, fake_sensor, alert_strategy=fake_alert)

    with pytest.raises(OutOfRangeError):
        service.record_reading(sensor_id=1, value=150.0, unit="C")

    assert fake_alert.alerts_triggered == [(1, 150.0, 75.0)]

def test_get_stats_by_sensor_success() -> None:
    """Cubre la obtención exitosa de estadísticas en la capa de negocio."""
    mock_reading_repo = MagicMock()
    mock_sensor_repo = MagicMock()
    
    # Simulamos que el sensor existe y está activo
    mock_sensor = MagicMock()
    mock_sensor.is_active = True
    mock_sensor_repo.get_by_id.return_value = mock_sensor
    
    # Simulamos la respuesta del repositorio de lecturas
    mock_reading_repo.stats_for_sensor.return_value = {"minimum": 5.0, "maximum": 10.0, "average": 7.5}
    
    service = ReadingService(mock_reading_repo, mock_sensor_repo)
    result = service.get_stats_by_sensor(sensor_id=1)
    
    assert result["minimum"] == 5.0
    assert result["average"] == 7.5
    assert mock_reading_repo.stats_for_sensor.called

def test_get_stats_by_sensor_not_found() -> None:
    """Cubre la excepción cuando se piden estadísticas de un sensor inexistente."""
    mock_reading_repo = MagicMock()
    mock_sensor_repo = MagicMock()
    mock_sensor_repo.get_by_id.return_value = None  # Sensor no existe
    
    service = ReadingService(mock_reading_repo, mock_sensor_repo)
    
    with pytest.raises(SensorNotFoundError):
        service.get_stats_by_sensor(sensor_id=999)
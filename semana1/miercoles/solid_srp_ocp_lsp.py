"""
Módulo que implementa los principios SOLID (S, O y L) en el dominio de sensores,
respetando estrictamente las interfaces y especificaciones de la guía del curso.
"""
from abc import ABC, abstractmethod
from typing import Any

# Importamos la estructura de datos que definimos en nuestro sistema
from semana1.lunes.modelos_sensor import Reading as SensorReading
from semana1.lunes.modelos_sensor import SensorStatus, SensorType

# ==========================================================================
# S - Una clase, una responsabilidad: SensorReader lee; DataLogger persiste.
# ==========================================================================

# --- MAL (Violación de SRP: Una sola clase lee y persiste) ---
class BadSensorNode:
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id
        self.db_storage: list[Any] = []

    def read_and_save(self, val: float) -> None:
        # Lee y al mismo tiempo gestiona persistencia
        self.db_storage.append({"id": self.sensor_id, "val": val})


# --- BIEN (Responsabilidades segregadas según especificación) ---
class SensorReader:
    """Responsabilidad única: Lee datos físicos y los transforma en SensorReading."""
    def __init__(self, sensor_id: str, sensor_type: SensorType, unit: str) -> None:
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit

    def read(self, value: float) -> SensorReading:
        return SensorReading(0.0, self.sensor_id, self.sensor_type, value, SensorStatus.OK, self.unit)


class DataLogger:
    """Responsabilidad única: Persistir objetos SensorReading."""
    def __init__(self) -> None:
        self._storage: list[SensorReading] = []

    def persist(self, reading: SensorReading) -> None:
        self._storage.append(reading)

    def get_logs(self) -> list[SensorReading]:
        return self._storage


# ================================================================================================================
# O - AlertStrategy (ABC) con ConsoleAlert y FileAlert: agregar EmailAlert; el mañana NO toca el código existente.
# ================================================================================================================

# --- MAL (Violación de OCP: Modificar código condicional para nuevas alertas) ---
class BadAnomalyDetector:
    def __init__(self, alert_type: str, threshold: float) -> None:
        self.alert_type = alert_type
        self.threshold = threshold
        self.sent: list[str] = []

    def check(self, reading: SensorReading) -> None:
        if reading.value > self.threshold:
            if self.alert_type == "console":
                self.sent.append(f"Consola: Anomalia en {reading.sensor_id}")
            elif self.alert_type == "file":
                self.sent.append(f"Archivo: Anomalia en {reading.sensor_id}")
            # Si mañana agregamos Email, obligatoriamente tendríamos que modificar este método.


# --- BIEN (Código original de la guía intacto + implementaciones extensibles) ---
class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...


class ConsoleAlert(AlertStrategy):
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(f"CONSOLE: {message}")


class FileAlert(AlertStrategy):
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(f"FILE: {message}")


class AnomalyDetector:
    """Código intacto de la guía. Está cerrado a modificación pero abierto a extensión."""
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold

    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalia en {reading.sensor_id}")


# ===================================================================================================================================================
# L - TemperatureSensor y HumiditySensor son intercambiables donde se espera; BaseSensor: process_sensor(sensor: BaseSensor) funciona con cualquiera.
# ===================================================================================================================================================

class BaseSensor(ABC):
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id

    @abstractmethod
    def get_reading(self) -> SensorReading: ...


# --- MAL (Violación de LSP: Cambia el comportamiento esperado por el cliente) ---
class BadBrokenSensor(BaseSensor):
    def get_reading(self) -> SensorReading:
        # Viola el contrato al retornar None o lanzar una excepción no esperada en la interfaz
        raise NotImplementedError("Sensor no disponible por hardware fallido")


# --- BIEN (Subclases 100% intercambiables según especificación) ---
class TemperatureSensor(BaseSensor):
    def get_reading(self) -> SensorReading:
        return SensorReading(0.0, self.sensor_id, SensorType.TEMPERATURE, 25.0, SensorStatus.OK, "C")


class HumiditySensor(BaseSensor):
    def get_reading(self) -> SensorReading:
        return SensorReading(0.0, self.sensor_id, SensorType.HUMIDITY, 60.0, SensorStatus.OK, "%")


def process_sensor(sensor: BaseSensor) -> str:
    """Función de la guía: Trabaja de forma transparente con cualquier subclase de BaseSensor."""
    reading = sensor.get_reading()
    return f"[{reading.sensor_id}] Valor: {reading.value}{reading.unit}"

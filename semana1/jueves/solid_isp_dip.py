"""
Módulo que implementa los principios SOLID: I (ISP) y D (DIP).
Demuestra segregación de interfaces e inversión de dependencias con Protocol.
"""
from typing import Protocol

from semana1.lunes.modelos_sensor import Reading as SensorReading

# =====================================================================
# I - PRINCIPIO DE SEGREGACIÓN DE INTERFACES (ISP)
# =====================================================================

# --- MAL (Interfaz gorda que obliga a implementar métodos innecesarios) ---
class FatSmartDevice(Protocol):
    def read(self) -> float: ...
    def write(self, val: float) -> None: ...
    def calibrate(self, offset: float) -> None: ...
    def reset(self) -> None: ...


# --- BIEN (Interfaces segregadas, pequeñas y especializadas) ---
class Readable(Protocol):
    """Contrato solo para dispositivos que permiten lectura."""
    def read(self) -> float: ...


class Writable(Protocol):
    """Contrato solo para dispositivos que reciben datos o comandos."""
    def write(self, val: float) -> None: ...


class Calibratable(Protocol):
    """Contrato solo para sensores o actuadores que soportan calibración de offset."""
    def calibrate(self, offset: float) -> None: ...


# --- Implementaciones limpias que usan solo lo que necesitan ---
class SimpleADCSensor:
    """Un ADC básico es de solo lectura: únicamente implementa Readable."""
    def __init__(self, pin: int) -> None:
        self.pin = pin

    def read(self) -> float:
        return 3.3  # Valor simulado leído del hardware


class SmartActuator:
    """Un actuador inteligente implementa Writable y Calibratable, pero no Readable."""
    def __init__(self) -> None:
        self._val: float = 0.0
        self._offset: float = 0.0

    def write(self, val: float) -> None:
        self._val = val + self._offset

    def calibrate(self, offset: float) -> None:
        self._offset = offset

    @property
    def current_val(self) -> float:
        return self._val


# =====================================================================
# D - PRINCIPIO DE INVERSIÓN DE DEPENDENCIAS (DIP)
# =====================================================================

# --- Abstracción ---
class DataRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
    def get_latest(self, sensor_id: str) -> SensorReading | None: ...


# --- Módulo de Alto Nivel ---
class DataProcessor:
    """
    Depende de la abstracción (DataRepository), no de una implementación concreta.
    Esto permite inyectar cualquier repositorio sin alterar esta lógica.
    """
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository  # Inyección de dependencias

    def process_and_save(self, reading: SensorReading) -> str:
        """Procesa una lectura y la delega al repositorio inyectado."""
        self._repo.save(reading)
        return f"Exito: [{reading.sensor_id}] guardado con valor {reading.value}"

    def get_last_reading(self, sensor_id: str) -> SensorReading | None:
        """Solicita la última lectura al repositorio abstracto."""
        return self._repo.get_latest(sensor_id)


# --- Implementación de Bajo Nivel para Tests (Simulación en RAM) ---
class InMemoryRepository:
    """
    Implementación en memoria (sin base de datos real) para pruebas rápidas y aisladas.
    Al cumplir el contrato DataRepository, es 100% compatible con DataProcessor.
    """
    def __init__(self) -> None:
        # Diccionario que mapea sensor_id hacia una lista de lecturas
        self._storage: dict[str, list[SensorReading]] = {}

    def save(self, reading: SensorReading) -> None:
        if reading.sensor_id not in self._storage:
            self._storage[reading.sensor_id] = []
        self._storage[reading.sensor_id].append(reading)

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        readings = self._storage.get(sensor_id)
        if not readings:
            return None
        return readings[-1]

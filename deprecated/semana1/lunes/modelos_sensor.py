"""
Módulo de modelos de dominio para sensores.
Implementa estructuras de datos inmutables y fuertemente tipadas.
"""
import random
import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol


class SensorType(Enum):
    """Tipos de sensores soportados por el sistema."""
    TEMPERATURE = auto()
    HUMIDITY = auto()
    PRESSURE = auto()
    VOLTAGE = auto()


class SensorStatus(Enum):
    """Estado operativo de la lectura o del hardware."""
    OK = auto()
    ERROR = auto()
    CALIBRATING = auto()
    DISCONNECTED = auto()


@dataclass(frozen=True)
class Reading:
    """
    Representa una lectura inmutable obtenida de un sensor.
    Al ser frozen=True, actúa como un registro de solo lectura (thread-safe y sin efectos secundarios).
    """
    timestamp: float        # Marca de tiempo en segundos (estilo Unix timestamp o time.monotonic)
    sensor_id: str          # Identificador único (ej. "DHT22_01", "ADC_CH3")
    sensor_type: SensorType # Tipo de variable física
    value: float            # Valor medido
    status: SensorStatus    # Estado del hardware al medir
    unit: str               # Unidad de medida ("C", "%", "hPa", "V")
    error_msg: str | None = None  # Mensaje opcional si status == ERROR

class Sensor(Protocol):
    """
    Interfaz estructural (HAL) para cualquier sensor en el sistema.
    Cualquier clase que implemente los métodos read() y get_id() será
    considerada un 'Sensor' por mypy, ¡sin necesidad de heredar de esta clase!
    """
    def read(self) -> Reading:
        """Obtiene una nueva lectura del hardware o simulación."""
        ...

    def get_id(self) -> str:
        """Devuelve el identificador único del sensor."""
        ...


class DummyTempSensor:
    """
    Driver simulado para un sensor de temperatura.
    Fíjate que NO escribimos 'class DummyTempSensor(Sensor):'.
    Al implementar read() y get_id(), cumple implícitamente con el Protocolo Sensor.
    """
    def __init__(self, sensor_id: str):
        # El guion bajo inicial indica convención de atributo protegido/privado en Python
        self._id = sensor_id

    def get_id(self) -> str:
        return self._id

    def read(self) -> Reading:
        # Simulamos una lectura aleatoria entre 20.0 y 25.0 grados
        val = round(random.uniform(20.0, 25.0), 2)
        return Reading(
            timestamp=time.time(),
            sensor_id=self._id,
            sensor_type=SensorType.TEMPERATURE,
            value=val,
            status=SensorStatus.OK,
            unit="C"
        )
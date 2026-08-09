"""
Módulo de procesamiento puro para lecturas de sensores.
Todas las funciones aquí son sin efectos secundarios (pure functions).
"""
from collections.abc import Sequence
from dataclasses import replace

from semana1.lunes.modelos_sensor import Reading, SensorStatus, SensorType


def convert_temperature_c_to_f(reading: Reading) -> Reading:
    """
    Convierte una lectura de temperatura de Celsius a Fahrenheit.
    Devuelve una NUEVA instancia de Reading con el valor y unidad actualizados.
    """
    if reading.sensor_type != SensorType.TEMPERATURE or reading.unit != "C":
        return reading

    new_val = round((reading.value * 9 / 5) + 32, 2)
    # replace() crea un clon inmutable cambiando solo los atributos especificados
    return replace(reading, value=new_val, unit="F")


def calibrate_reading(reading: Reading, gain: float, offset: float) -> Reading:
    """
    Aplica una ecuación lineal de calibración: y = (x * gain) + offset.
    Devuelve una nueva lectura calibrada.
    """
    calibrated_val = round((reading.value * gain) + offset, 4)
    return replace(reading, value=calibrated_val)


def filter_valid_readings(readings: Sequence[Reading]) -> list[Reading]:
    """
    Filtra una lista/secuencia de lecturas y retorna solo aquellas que tienen estado OK.
    """
    return [r for r in readings if r.status == SensorStatus.OK]


def calculate_moving_average(readings: Sequence[Reading]) -> float:
    """
    Calcula el promedio aritmético de los valores en una secuencia de lecturas.
    Si la lista está vacía, devuelve 0.0 para evitar ZeroDivisionError.
    """
    if not readings:
        return 0.0
    
    total = sum(r.value for r in readings)
    return round(total / len(readings), 2)


def detect_outliers(readings: Sequence[Reading], threshold: float) -> list[Reading]:
    """
    Retorna una lista con las lecturas cuyo valor absoluto supera un umbral dado
    (útil para disparar alarmas en un Event Loop).
    """
    return [r for r in readings if abs(r.value) > threshold]
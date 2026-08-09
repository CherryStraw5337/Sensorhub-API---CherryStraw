from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from semana2.eval1.models import SensorReading


class AlertStrategy(Protocol):
    """Contrato para cualquier estrategia de notificación de alertas."""
    def send(self, reading: SensorReading, anomaly_type: str) -> None:
        ...


class ConsoleAlertStrategy:
    """Estrategia que imprime las alertas directamente en la salida estándar."""
    def send(self, reading: SensorReading, anomaly_type: str) -> None:
        message = f"ALERTA: {anomaly_type} en {reading.sensor_id} [{reading.value}]"
        print(message)


class FileAlertStrategy:
    """Estrategia que persiste las alertas en un archivo de texto en modo append."""
    def __init__(self, file_path: Path | str) -> None:
        self.file_path = Path(file_path)

    def send(self, reading: SensorReading, anomaly_type: str) -> None:
        message = f"ALERTA: {anomaly_type} en {reading.sensor_id} [{reading.value}]\n"
        with open(self.file_path, mode="a", encoding="utf-8") as f:
            f.write(message)


class AlertManager:
    """Gestor centralizado que distribuye alertas a todas las estrategias configuradas."""
    def __init__(self, strategies: Sequence[AlertStrategy]) -> None:
        self.strategies = strategies

    def notify(self, reading: SensorReading, anomaly_type: str) -> None:
        if anomaly_type == "NORMAL":
            return
        for strategy in self.strategies:
            strategy.send(reading, anomaly_type)
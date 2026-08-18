# app/services/alert_strategy.py

from typing import Protocol


class AlertStrategy(Protocol):
    """Protocolo OCP para las estrategias de notificación de anomalías"""
    def trigger_alert(self, id: int, reading_value: float, threshold: float) -> None:
        ...
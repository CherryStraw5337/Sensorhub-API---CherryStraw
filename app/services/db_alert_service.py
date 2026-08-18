# app/services/db_alert_strategy.py
from app.repositories.alert_repo import AlertRepository


class DatabaseAlertStrategy:
    """Estrategia concreta que persiste alertas usando el AlertRepository."""

    def __init__(self, alert_repo: AlertRepository) -> None:
        self.alert_repo = alert_repo

    def trigger_alert(self, id: int, reading_value: float, threshold: float, message: str = "Alerta de anomalía detectada") -> None:
        self.alert_repo.add(
            id=id,
            reading_value=reading_value,
            threshold=threshold,
            message=message
        )
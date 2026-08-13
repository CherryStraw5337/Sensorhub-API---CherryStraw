# app/repositories/alert_repo.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import AlertModel


class AlertRepository:
    """Repositorio para gestionar el acceso a datos de alertas/anomalías."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, sensor_id: int, reading_value: float, threshold: float, message: str = "Alerta de anomalía detectada") -> AlertModel:
        """Guarda un nuevo registro de alerta en la base de datos."""
        alert = AlertModel(
            sensor_id=sensor_id,
            reading_value=reading_value,
            threshold=threshold,
            message=message
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def list_for_sensor(self, sensor_id: int, limit: int = 50, offset: int = 0) -> list[AlertModel]:
        """Obtiene las alertas filtradas por sensor con paginación."""
        stmt = (
            select(AlertModel)
            .where(AlertModel.sensor_id == sensor_id)
            .order_by(AlertModel.timestamp.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())
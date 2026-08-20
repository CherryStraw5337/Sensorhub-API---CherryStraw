# app/repositories/alert_repo.py

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import AlertModel
from app.models.sensor import SensorModel


class AlertRepository:
    """Repositorio para gestionar el acceso a datos de alertas/anomalías."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, id: int, reading_value: float, threshold: float, alarm_type: str = "threshold_breached", message: str = "Alerta de anomalía detectada") -> AlertModel:
        alert = AlertModel(
            id=id,
            reading_value=reading_value,
            threshold=threshold,
            alarm_type=alarm_type,
            message=message
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    # 1. BIBLIOTECA GENERAL DE ALARMAS
    def get_all_alerts(self, limit: int = 50, offset: int = 0, is_resolved: bool | None = None) -> list[AlertModel]:
        """Obtiene todas las alarmas históricas de la plataforma, opcionalmente filtradas por estado de resolución."""
        stmt = select(AlertModel)
        if is_resolved is not None:
            stmt = stmt.where(AlertModel.is_resolved == is_resolved)
            
        stmt = stmt.order_by(AlertModel.timestamp.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt).all())

    # 2. HISTORIAL DE ALARMAS DE UN SOLO SENSOR
    def list_for_sensor(self, id: int, limit: int = 50, offset: int = 0) -> list[AlertModel]:
        stmt = (
            select(AlertModel)
            .where(AlertModel.id == id)
            .order_by(AlertModel.timestamp.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    # 3. BÚSQUEDA AVANZADA: OBTENER SENSORES CON ALARMAS RECIENTES
    def get_sensors_by_recent_alarm(self, alarm_type: str, hours: int = 24) -> list[SensorModel]:
        """Devuelve los sensores (únicos) que han detonado un tipo de alarma específico en las últimas X horas."""
        time_threshold = datetime.now(UTC) - timedelta(hours=hours)
        
        stmt = (
            select(SensorModel)
            .join(AlertModel) # Hacemos JOIN entre Sensor y Alarma
            .where(AlertModel.alarm_type == alarm_type)
            .where(AlertModel.timestamp >= time_threshold)
            .distinct() # Si un sensor falló 5 veces hoy, lo devolvemos solo 1 vez
        )
        return list(self.db.scalars(stmt).all())
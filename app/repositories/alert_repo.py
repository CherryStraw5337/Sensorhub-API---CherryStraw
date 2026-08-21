# app/repositories/alert_repo.py

from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from app.models.alert import AlertModel


class AlertRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(
        self,
        sensor_id: int,
        reading_value: float,
        threshold: float | None = None,
        message: str = "Alerta de anomalía detectada",
    ) -> AlertModel:
        db_alert = AlertModel(
            sensor_id=sensor_id,
            reading_value=reading_value,
            threshold=threshold if threshold is not None else reading_value,
            message=message
            # 'status' se autocompleta con "open" por defecto gracias al Modelo
        )
        self._session.add(db_alert)
        self._session.commit()
        self._session.refresh(db_alert)
        return db_alert

    def get_all_alerts(
        self,
        limit: int = 50,
        offset: int = 0,
        is_resolved: bool | None = None,
    ) -> list[AlertModel]:
        stmt = select(AlertModel).order_by(desc(AlertModel.timestamp), desc(AlertModel.id))
        if is_resolved is not None:
            status_value = "resolved" if is_resolved else "open"
            stmt = stmt.where(AlertModel.status == status_value)
        result = self._session.scalars(stmt.offset(offset).limit(limit)).all()
        return list(result)

    def list_for_sensor(self, sensor_id: int, limit: int = 10, offset: int = 0) -> list[AlertModel]:
        stmt = select(AlertModel).where(AlertModel.sensor_id == sensor_id).offset(offset).limit(limit)
        result = self._session.scalars(stmt).all()
        return list(result)

    # NUEVO MÉTODO: Actualizar el estado
    def update_status(self, alert_id: int, new_status: str) -> AlertModel | None:
        db_alert = self._session.get(AlertModel, alert_id)
        if not db_alert:
            return None

        db_alert.status = new_status  # type: ignore[assignment]
        self._session.commit()
        self._session.refresh(db_alert)
        return db_alert
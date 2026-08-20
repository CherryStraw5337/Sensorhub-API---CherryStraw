# app/routers/alerts.py

from typing import Annotated

import fastapi
from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.alert_repo import AlertRepository
from app.schemas.alert import AlertOut
from app.schemas.sensor import SensorOut

router = fastapi.APIRouter(tags=["Alertas"])
DbSession = Annotated[Session, Depends(get_db)]

@router.get("/alerts/", response_model=list[AlertOut])
def get_alerts_library(
    limit: int = fastapi.Query(50, ge=1),
    offset: int = fastapi.Query(0, ge=0),
    is_resolved: bool | None = fastapi.Query(None, description="Filtrar por estado de resolución de la alarma"),
    *,
    db: DbSession
) -> list[AlertOut]:
    """Biblioteca general de alarmas de toda la infraestructura IoT."""
    repo = AlertRepository(db)
    return repo.get_all_alerts(limit=limit, offset=offset, is_resolved=is_resolved) # type: ignore

@router.get("/alerts/sensors-by-alarm", response_model=list[SensorOut])
def get_sensors_by_recent_alarm(
    alarm_type: str = fastapi.Query(..., description="Tipo de alarma (ej: threshold_breached)"),
    hours: int = fastapi.Query(24, ge=1, description="Ventana de tiempo en horas hacia atrás"),
    *,
    db: DbSession
) -> list[SensorOut]:
    """Devuelve los sensores únicos que dispararon una alarma específica en las últimas X horas."""
    repo = AlertRepository(db)
    return repo.get_sensors_by_recent_alarm(alarm_type=alarm_type, hours=hours) # type: ignore

@router.get("/sensors/{sensor_id}/alerts", response_model=list[AlertOut])
def list_sensor_alerts(
    sensor_id: int,
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    *,
    db: DbSession,
) -> list[AlertOut]:
    """Obtiene el historial de alertas de un sensor específico."""
    repo = AlertRepository(db)
    return repo.list_for_sensor(sensor_id, limit=limit, offset=offset)  # type: ignore
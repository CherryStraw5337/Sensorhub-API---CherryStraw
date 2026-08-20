# app/routers/readings.py

from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.alert_repo import AlertRepository
from app.repositories.reading_repo import SQLAlchemyReadingRepository
from app.repositories.sensor_repo import SensorRepository
from app.schemas.reading import ReadingCreate, ReadingOut
from app.services.db_alert_service import DatabaseAlertStrategy
from app.services.reading_service import ReadingService

router = APIRouter(tags=["Readings"])

get_db_dependency = Depends(get_db)

def get_reading_service(db: Session = get_db_dependency) -> ReadingService:
    reading_repo = SQLAlchemyReadingRepository(db)
    sensor_repo = SensorRepository(db)
    alert_repo = AlertRepository(db)
    alert_strategy = DatabaseAlertStrategy(alert_repo)
    return ReadingService(
        reading_repo=reading_repo,
        sensor_repo=sensor_repo,
        alert_strategy=alert_strategy,
    )

get_reading_service_dependency = Depends(get_reading_service)

@router.post("/readings/", response_model=ReadingOut, status_code=status.HTTP_201_CREATED)
def create_reading(
    payload: ReadingCreate,
    service: ReadingService = get_reading_service_dependency,
) -> ReadingOut:
    """Ingresa una nueva lectura de telemetría, validando física y generando alarma si es anómala."""
    return service.record_reading(payload.id, payload.value, payload.unit)  # type: ignore

@router.get("/readings/", response_model=list[ReadingOut])
def search_readings(
    limit: int | None = None,
    offset: int | None = None,
    sensor_type: str | None = None,
    location: str | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    is_anomalous: bool | None = None,
    db: Session = get_db_dependency,
) -> list[ReadingOut]:
    """Búsqueda avanzada global de lecturas combinando filtros de sensores y tiempos."""
    if limit is None:
        limit = Query(50, ge=1)
    if offset is None:
        offset = Query(0, ge=0)
    if sensor_type is None:
        sensor_type = Query(None, description="Tipo de sensor (ej: TEMPERATURE)")
    if location is None:
        location = Query(None, description="Ubicación o parte de ella")
    if from_date is None:
        from_date = Query(None, alias="from", description="Fecha/hora de inicio (ISO)")
    if to_date is None:
        to_date = Query(None, alias="to", description="Fecha/hora de fin (ISO)")
    if is_anomalous is None:
        is_anomalous = Query(None, description="Filtrar si superó el umbral")
    
    repo = SQLAlchemyReadingRepository(db)
    return repo.search_readings(
        limit=limit,
        offset=offset,
        sensor_type=sensor_type,
        location=location,
        from_date=from_date,
        to_date=to_date,
        is_anomalous=is_anomalous
    )  # type: ignore
# app/routers/readings.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.alert_repo import AlertRepository
from app.repositories.reading_repo import SQLAlchemyReadingRepository
from app.repositories.sensor_repo import SensorRepository
from app.schemas.reading import ReadingCreate, ReadingOut, ReadingUpdate
from app.services.db_alert_strategy import DatabaseAlertStrategy
from app.services.errors_service import OutOfRangeError
from app.services.reading_service import ReadingService

"""Router para manejar las operaciones relacionadas con lecturas."""
router = APIRouter(tags=["Lecturas"])

get_db_dependency = Depends(get_db)
get_from = Query(None, alias="from")
get_to = Query(None, alias="to")


def get_reading_service(db: Session = get_db_dependency) -> ReadingService:
    """
    Dependencia para instanciar ReadingService con sus repositorios
    y la estrategia de alertas conectada a la Base de Datos.
    """
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

"""Endpoints siguiendo las convenciones REST"""


class LecturaLegacy(BaseModel):
    id: int
    value: float
    unit: str | None = None


@router.post("/readings/", response_model=ReadingOut, status_code=201)
def crear_lectura_legacy(
    payload: LecturaLegacy,
    service: ReadingService = get_reading_service_dependency,
) -> ReadingOut:
    """Mantiene la ruta antigua de ingesta para clientes existentes."""
    sensor = service._sensor_repo.get_by_id(payload.id)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    unidad = payload.unit or sensor.unit
    try:
        lectura = service.record_reading(payload.id, payload.value, unidad)
    except OutOfRangeError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Valor fuera de los límites físicos: {exc}",
        ) from exc
    return ReadingOut.model_validate(lectura, from_attributes=True)


@router.get("/sensors/{sensor_id}/readings", response_model=list[ReadingOut])
def list_sensor_readings(
    sensor_id: int,
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    from_date: datetime | None = get_from,
    to_date: datetime | None = get_to,
    service: ReadingService = get_reading_service_dependency,
) -> list[ReadingOut]:
    """Lista lecturas de un sensor con paginación y filtros de fecha"""
    return service.get_readings_by_sensor(sensor_id, limit, offset, from_date, to_date)  # type: ignore


@router.post("/sensors/{sensor_id}/readings", response_model=ReadingOut, status_code=201)
def create_reading(
    sensor_id: int,
    payload: ReadingCreate,
    service: ReadingService = get_reading_service_dependency,
) -> ReadingOut:
    """Crea una nueva lectura validando límites físicos y generando alerta si hay anomalía"""
    return service.record_reading(sensor_id, payload.value, payload.unit)  # type: ignore


@router.get("/readings/{reading_id}", response_model=ReadingOut)
def get_reading(
    reading_id: int,
    service: ReadingService = get_reading_service_dependency,
) -> ReadingOut:
    """Obtiene una lectura específica por su ID único"""
    return service.get_reading(reading_id)  # type: ignore


@router.patch("/readings/{reading_id}", response_model=ReadingOut)
def update_reading(
    reading_id: int,
    payload: ReadingUpdate,
    service: ReadingService = get_reading_service_dependency,
) -> ReadingOut:
    """Actualiza parcialmente una lectura existente"""
    return service.update_reading(reading_id, payload)  # type: ignore


@router.delete("/readings/{reading_id}", status_code=204)
def delete_reading(
    reading_id: int,
    service: ReadingService = get_reading_service_dependency,
) -> None:
    """Elimina una lectura por su ID"""
    service.delete_reading(reading_id)
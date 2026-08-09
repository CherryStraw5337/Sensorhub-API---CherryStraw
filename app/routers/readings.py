from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.reading_repo import SQLAlchemyReadingRepository
from app.repositories.sensor_repo import SensorRepository
from app.schemas.reading import ReadingCreate, ReadingOut, ReadingUpdate
from app.services.reading_service import ReadingService

"""Router para manejar las operaciones relacionadas con lecturas"""
router = APIRouter(tags=["Readings"])

get_db_dependency = Depends(get_db)
get_from = Query(None, alias="from")
get_to = Query(None, alias="to")

def get_reading_service(db: Session = get_db_dependency) -> ReadingService:
    """Dependencia para obtener una instancia de ReadingService con sus repositorios"""
    reading_repo = SQLAlchemyReadingRepository(db)
    sensor_repo = SensorRepository(db)
    return ReadingService(reading_repo, sensor_repo)

get_reading_service_dependency = Depends(get_reading_service)

"""Endpoints siguiendo las convenciones REST de la Semana 3"""

@router.get("/sensors/{sensor_id}/readings", response_model=list[ReadingOut])
def list_sensor_readings(
    sensor_id: int,
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    from_date: datetime | None = get_from,
    to_date: datetime | None = get_to,
    service: ReadingService = get_reading_service_dependency
) -> list[ReadingOut]:
    """Lista lecturas de un sensor con paginación y filtros de fecha"""
    return service.get_readings_by_sensor(sensor_id, limit, offset, from_date, to_date) # type: ignore

@router.post("/sensors/{sensor_id}/readings", response_model=ReadingOut, status_code=201)
def create_reading(
    sensor_id: int,
    payload: ReadingCreate,
    service: ReadingService = get_reading_service_dependency
) -> ReadingOut:
    """Crea una nueva lectura validando límites físicos en la capa de servicio"""
    return service.record_reading(sensor_id, payload.value, payload.unit) # type: ignore

@router.get("/readings/{reading_id}", response_model=ReadingOut)
def get_reading(
    reading_id: int, 
    service: ReadingService = get_reading_service_dependency
) -> ReadingOut:
    """Obtiene una lectura específica por su ID único"""
    return service.get_reading(reading_id) # type: ignore

@router.patch("/readings/{reading_id}", response_model=ReadingOut)
def update_reading(
    reading_id: int, 
    payload: ReadingUpdate, 
    service: ReadingService = get_reading_service_dependency
) -> ReadingOut:
    """Actualiza parcialmente una lectura existente"""
    return service.update_reading(reading_id, payload) # type: ignore

@router.delete("/readings/{reading_id}", status_code=204)
def delete_reading(
    reading_id: int, 
    service: ReadingService = get_reading_service_dependency
) -> None:
    """Elimina (o desactiva) una lectura del sistema"""
    return service.delete_reading(reading_id)
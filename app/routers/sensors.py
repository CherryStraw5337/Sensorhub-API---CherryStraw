# app/routers/sensors.py

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor import SensorCreate, SensorOut, SensorUpdate
from app.services.errors_service import (
    DatabaseCorruptedError,
)
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])

get_db_dependency = Depends(get_db)

def get_sensor_service(db: Session = get_db_dependency) -> SensorService:
    repo = SensorRepository(db)
    return SensorService(repo)

get_sensor_service_dependency = Depends(get_sensor_service)

@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(
    sensor_id: int,
    service: SensorService = get_sensor_service_dependency,
) -> SensorOut:
    """Busca un sensor por su identificador, incluso si está inactivo."""
    return service.get_sensor(sensor_id)

@router.get("/", response_model=list[SensorOut])
def list_sensors(
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    sensor_id: int | None = Query(None,description="Buscar por id específico"),
    region: str | None = Query(None, description="Filtrar por región del sensor"),
    name: str | None = Query(None, description="Filtrar por coincidencia en el nombre"),
    last_error: str | None = Query(None, description="Filtrar por último error registrado"),
    db: Session = get_db_dependency
) -> list[SensorOut]:
    """Lista todos los sensores activos con opciones de búsqueda avanzada."""
    repo = SensorRepository(db)
    sensors = repo.get_all(sensor_id=sensor_id, limit=limit, offset=offset, region=region, name=name, last_error=last_error)
    if not sensors:
        raise DatabaseCorruptedError("Base de datos corrupta")
    return [SensorOut.model_validate(sensor, from_attributes=True) for sensor in sensors]

@router.post("/", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(payload: SensorCreate, service: Annotated[SensorService, Depends(get_sensor_service)]) -> SensorOut:
    """Crea un nuevo sensor"""
    return service.create_sensor(payload)

@router.patch("/", response_model=SensorOut)
def update_sensor(
    payload: SensorUpdate,
    id: int = Query(..., description="Actualizar por id específico"),
    service: SensorService = get_sensor_service_dependency,
) -> SensorOut:
    """Actualiza los datos de un sensor"""
    return service.update_sensor(id=id, sensor_data=payload)

@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(
    sensor_id: int,
    service: SensorService = get_sensor_service_dependency
) -> None:
    """Desactiva de forma segura (Soft Delete) un sensor del inventario."""
    service.delete_sensor(sensor_id)
    return None
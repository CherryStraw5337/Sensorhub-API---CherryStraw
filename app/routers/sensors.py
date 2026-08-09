from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor import SensorCreate, SensorOut, SensorUpdate
from app.services.sensor_service import SensorService

"""Router para manejar las operaciones relacionadas con sensores"""
router = APIRouter(prefix="/sensors", tags=["Sensors"])

get_db_dependency = Depends(get_db)

def get_sensor_service(db: Session = get_db_dependency) -> SensorService:
    """Dependencia para obtener una instancia de SensorService"""
    repo = SensorRepository(db)
    return SensorService(repo)

get_sensor_service_dependency = Depends(get_sensor_service)

"""Endpoints para manejar las operaciones CRUD de sensores"""

@router.get("/", response_model=list[SensorOut])
def list_sensors(
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    service: SensorService = get_sensor_service_dependency
) -> list[SensorOut]:
    # El servicio devuelve List[SensorModel], FastAPI lo convertirá a List[SensorOut]
    return service.get_sensors(limit, offset) # type: ignore

@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(
    sensor_id: int, 
    service: SensorService = get_sensor_service_dependency
) -> SensorOut:
    return service.get_sensor(sensor_id) # type: ignore

@router.post("/", response_model=SensorOut, status_code=201)
def create_sensor(
    payload: SensorCreate, 
    service: Annotated[SensorService, Depends(get_sensor_service)] # Usar Annotated
) -> SensorOut:
    return service.create_sensor(payload) # type: ignore

@router.patch("/{sensor_id}", response_model=SensorOut)
def update_sensor(
    sensor_id: int, 
    payload: SensorUpdate, 
    service: SensorService = get_sensor_service_dependency
) -> SensorOut:
    return service.update_sensor(sensor_id, payload) # type: ignore

@router.delete("/{sensor_id}", status_code=204)
def delete_sensor(
    sensor_id: int, 
    service: SensorService = get_sensor_service_dependency
) -> None:
    return service.delete_sensor(sensor_id)
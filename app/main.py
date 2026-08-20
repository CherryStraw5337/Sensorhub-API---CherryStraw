from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import Base, ensure_sqlite_schema, engine
from app.routers import alerts, readings, sensors
from app.services.errors_service import (
    InvalidUnitError,
    OutOfRangeError,
    ReadingNotFoundError,
    SensorNotFoundError,
)
from app.models.alert import AlertModel
from app.models.reading import ReadingModel
from app.models.sensor import SensorModel

"""Fabricación de la base de datos (semana 4 usaremos Alembic)"""
ensure_sqlite_schema()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SensorHub API",
    description="API completa con arquitectura en 4 capas y validación física.",
    version="1.0.0"
)

"""Inclusión de Routers"""
app.include_router(sensors.router)
app.include_router(readings.router)
app.include_router(alerts.router)

@app.get("/health", tags=["System"])
def health() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return {"status": "degraded", "service": "SensorHub", "database": "error"}

    return {"status": "ok", "service": "SensorHub", "database": "ok"}


@app.get("/metrics", tags=["System"])
def metrics() -> dict[str, int]:
    with Session(engine) as session:
        return {
            "active_sensors": session.scalar(
                select(func.count()).select_from(SensorModel).where(SensorModel.is_active.is_(True))
            ) or 0,
            "readings_total": session.scalar(
                select(func.count()).select_from(ReadingModel)
            ) or 0,
            "open_alerts": session.scalar(
                select(func.count()).select_from(AlertModel).where(AlertModel.status == "open")
            ) or 0,
        }

@app.exception_handler(SensorNotFoundError)
@app.exception_handler(ReadingNotFoundError)
async def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(InvalidUnitError)
async def invalid_unit_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.exception_handler(OutOfRangeError)
async def out_of_range_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})
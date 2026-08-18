# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.db import Base, engine
from app.routers import alerts, readings, sensors
from app.services.errors_service import (
    AlertNotFoundError,
    InvalidUnitError,
    OutOfRangeError,
    ReadingNotFoundError,
    SensorNotFoundError,
    UndocumentedError,
)

# Instancia principal de la aplicación FastAPI
# (Ya no usamos 'api' de 'mypy')
app = FastAPI(title="SensorHub API", version="1.0.0")

"""Fabricación de la base de datos (semana 4 usaremos Alembic)"""
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
    return {"status": "ok", "service": "SensorHub"}

@app.exception_handler(SensorNotFoundError)
@app.exception_handler(ReadingNotFoundError)
@app.exception_handler(AlertNotFoundError)
async def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(InvalidUnitError)
async def invalid_unit_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.exception_handler(OutOfRangeError)
async def out_of_range_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})

@app.exception_handler(UndocumentedError)
async def undocumented_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(satus_code=500, content={"detail": str(exc)})
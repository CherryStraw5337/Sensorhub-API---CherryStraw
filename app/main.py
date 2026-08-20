from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.db import Base, ensure_sqlite_schema, engine
from app.routers import readings, sensors
from app.services.errors_service import (
    InvalidUnitError,
    OutOfRangeError,
    ReadingNotFoundError,
    SensorNotFoundError,
)

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

@app.get("/health", tags=["System"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "SensorHub"}

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
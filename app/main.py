from fastapi import FastAPI

from app.db import Base, engine
from app.routers import readings, sensors

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

@app.get("/health", tags=["System"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "SensorHub"}
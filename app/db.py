# app/db.py

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# 1. Normalizador de URL (Vital para Render y Docker)
def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

DATABASE_URL = get_database_url()

# 2. Configuración del Engine
# SQLite necesita check_same_thread, pero PostgreSQL fallaría si se lo pasamos.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

def ensure_sqlite_schema() -> None:
    """Añade columnas nuevas cuando se reutiliza una base SQLite antigua."""
    if not DATABASE_URL.startswith("sqlite"):
        return

    with engine.begin() as connection:
        existe = connection.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='sensors'"
        ).fetchone()
        if existe is None:
            Base.metadata.create_all(bind=engine)
            return

        columnas = {
            fila[1]
            for fila in connection.exec_driver_sql("PRAGMA table_info('sensors')").fetchall()
        }
        actualizaciones = {
            "threshold": "REAL",
            "is_active": "BOOLEAN DEFAULT 1 NOT NULL",
            "location": "VARCHAR DEFAULT 'Desconocida' NOT NULL",
            "region": "VARCHAR",
            "last_error": "VARCHAR",
        }
        for nombre, tipo in actualizaciones.items():
            if nombre not in columnas:
                connection.exec_driver_sql(
                    f"ALTER TABLE sensors ADD COLUMN {nombre} {tipo}"
                )


# 3. Generador de sesión inyectable
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
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

# 3. Generador de sesión inyectable (Se mantiene igual)
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
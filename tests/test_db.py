import os
from unittest.mock import patch

from app.db import get_database_url, get_db


def test_get_database_url_postgres_replace() -> None:
    """Verifica que cambie postgres:// a postgresql+psycopg:// (Líneas 13-14)"""
    with patch.dict(os.environ, {"DATABASE_URL": "postgres://user:pass@localhost/db"}):
        url = get_database_url()
        assert url == "postgresql+psycopg://user:pass@localhost/db"

def test_get_database_url_postgresql_replace() -> None:
    """Verifica que agregue +psycopg si falta (Líneas 15-16)"""
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@localhost/db"}):
        url = get_database_url()
        assert url == "postgresql+psycopg://user:pass@localhost/db"

def test_get_db_yields_and_closes() -> None:
    """Verifica el ciclo de vida de la sesión (yield y close) (Líneas 34-38)"""
    gen = get_db()
    
    # Obtenemos la sesión del generador (ejecuta hasta el yield)
    session = next(gen)
    assert session is not None
    
    # Simulamos el cierre del generador (lo que hace FastAPI al final del request)
    try:
        next(gen)
    except StopIteration:
        pass
    
    # Si llegó aquí sin colgarse, cubrió el finally: db.close()
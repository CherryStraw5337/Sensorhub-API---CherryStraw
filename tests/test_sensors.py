# tests/test_sensors.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db

# Importamos la aplicación real y la base real
from app.main import app

# ==============================================================================
# CONFIGURACIÓN DE INFRAESTRUCTURA DE PRUEBAS (Temporalmente aquí)
# ==============================================================================

# 1. Configurar una base de datos SQLite EN MEMORIA para tests rápidos y aislados
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, # Necesario para persistir datos en memoria entre conexiones
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Fixture que crea las tablas antes del test y las borra después
@pytest.fixture(name="session")
def fixture_session():
    # Crear tablas físicas en la DB en memoria
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Borrar tablas para asegurar aislamiento del siguiente test
        Base.metadata.drop_all(bind=engine)

# 3. Fixture que sobrescribe la dependencia get_db de FastAPI e instancia el cliente
@pytest.fixture(name="client")
def fixture_client(session):
    # Sobrescritura de dependencia (Dependency Injection override)
    def override_get_db():
        try:
            yield session
        finally:
            pass # session.close() ya se maneja en la fixture anterior

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Limpiar sobrescrituras después del test
    app.dependency_overrides.clear()


# ==============================================================================
# TEST DE LA US-01: Registro exitoso de sensor nuevo (TDD ROJO)
# ==============================================================================

def test_create_sensor_success(client):
    """
    US-01 / RF-1: Verificar que un sensor nuevo se registre exitosamente
    con estado OK yis_active=True.
    """
    # GIVEN: Un payload válido para un sensor de temperatura
    payload = {
        "id": "TEMP_01",
        "location": "Warehouse A",
        "type": "TEMPERATURE",
        "alert_threshold": 35.0
    }

    # WHEN: El cliente envía una petición POST a /sensors/
    # Nota: Asumimos que el router en app/main.py está montado en /sensors
    response = client.post("/sensors/", json=payload)

    # THEN: La respuesta debe ser HTTP 201 Created
    assert response.status_code == 201, f"Fallo: {response.text}"

    # AND: El cuerpo de la respuesta debe contener los datos enviados e 'is_active'
    data = response.json()
    assert data["id"] == payload["id"]
    assert data["location"] == payload["location"]
    assert data["type"] == payload["type"]
    assert data["alert_threshold"] == payload["alert_threshold"]
    # Requisito RF-1: En producción no se borra, se desactiva. Por defecto, activo.
    assert data["is_active"] is True
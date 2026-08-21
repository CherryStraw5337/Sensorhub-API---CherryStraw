# tests/test_alerts.py

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

# Instanciamos el cliente globalmente para este archivo
client = TestClient(app)

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=test_engine)
Base.metadata.create_all(bind=test_engine)


@pytest.fixture(autouse=True)
def isolate_database_override() -> Generator[None, None, None]:
    global client
    overrides = app.dependency_overrides.copy()

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        yield
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(overrides)


# Modificamos la firma de la prueba para que NO reciba 'client' como parámetro
def test_alert_state_machine_transition() -> None:
    test_client = TestClient(app)

    # 1. GIVEN: Un sensor y una lectura anómala que genere una alerta
    sensor_res = test_client.post("/sensors/", json={
        "name": "Termometro Caldera",
        "type": "TEMPERATURE",
        "unit": "C",
        "min_value": 0.0,
        "max_value": 100.0
    })
    sensor_id = sensor_res.json()["id"]

    # Inyectamos una lectura fuera de rango (150 C)
    test_client.post("/readings/", json={
        "sensor_id": sensor_id,
        "value": 150.0
    })

    # 2. Recuperamos la alerta generada
    alerts_res = test_client.get("/alerts/")
    alerts = alerts_res.json()
    assert len(alerts) > 0, "El sistema debió generar al menos una alerta"

    alert_id = alerts[0]["id"]

    # Validamos que el estado inicial sea "open"
    assert alerts[0].get("status") == "open", "La alerta debe iniciar en estado 'open'"

    # 3. WHEN: El operador reconoce la alerta (ACKNOWLEDGED)
    patch_res = test_client.patch(f"/alerts/{alert_id}", json={"status": "acknowledged"})

    # 4. THEN: El sistema debe aceptar el cambio
    assert patch_res.status_code == 200, "El endpoint PATCH /alerts/{id} debe existir y aceptar la petición"
    assert patch_res.json()["status"] == "acknowledged", "El estado de la alerta no se actualizó"
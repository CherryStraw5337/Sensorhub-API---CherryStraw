from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

# 1. Base de datos en memoria con StaticPool para persistencia en el test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Función de override limpia
def override_get_db() -> Generator[SQLAlchemySession, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Aplicar el override ANTES de crear el cliente
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# 4. Crear tablas
Base.metadata.create_all(bind=engine)

def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_full_reading_lifecycle() -> None:
    # Crear un sensor primero para evitar errores de FK o validación física
    client.post("/sensors/", json={
        "name": "S1", "type": "T", "unit": "C", "min_value": 0, "max_value": 100
    })
    
    # Crear lectura (usando la ruta REST correcta)
    response = client.post(
        "/sensors/1/readings",
        json={"value": 25.0, "unit": "C"}
    )
    assert response.status_code == 201

# --- TESTS DE SENSORES (Ampliación para US-01 Soft Delete) ---

def test_desactivacion_segura_sensor_soft_delete() -> None:
    """
    Scenario: Desactivación segura de un sensor (Soft Delete)
    Valida que al hacer DELETE, el registro no desaparece, sino que cambia is_active a False.
    """
    # 1. GIVEN: un sensor que existe y está activo por defecto
    res_sensor = client.post("/sensors/", json={
        "name": "Sensor a Desactivar", "type": "T", "unit": "C", "min_value": 0, "max_value": 100
    })
    id = res_sensor.json()["id"]
    # Verificamos que arranca activo (asumiendo que tu esquema base lo tiene)
    assert res_sensor.json()["is_active"] is True 

    # 2. WHEN: el administrador envía una petición DELETE a /sensors/{id}
    # Según la US-01, esperamos un 204 No Content
    response = client.delete(f"/sensors/{id}")
    assert response.status_code == 204

    # 3. THEN: Verificamos que el registro SIGUE EXISTIENDO pero está INACTIVO
    response_get = client.get(f"/sensors/{id}")
    assert response_get.status_code == 200 # No debe dar 404
    sensor_data = response_get.json()
    assert sensor_data["is_active"] is False # Aquí es donde debería fallar si no hay soft delete
    assert sensor_data["name"] == "Sensor a Desactivar" # Los datos siguen ahí

def test_consulta_omitiendo_sensores_inactivos() -> None:
    """
    Scenario: Consulta omitiendo sensores inactivos
    Valida que GET /sensors/ solo devuelva los que tienen is_active=True
    """
    # 1. GIVEN: Creamos un sensor activo y uno inactivo (vía el test anterior)
    
    # Sensor 1 (Activo)
    client.post("/sensors/", json={
        "name": "Sensor Activo", "type": "T", "unit": "C", "min_value": 0, "max_value": 100
    })
    
    # Sensor 2 (Lo creamos e inmediatamente lo 'borramos' para que esté inactivo)
    res_to_delete = client.post("/sensors/", json={
        "name": "Sensor Inactivo", "type": "T", "unit": "C", "min_value": 0, "max_value": 100
    })
    id_inactivo = res_to_delete.json()["id"]
    client.delete(f"/sensors/{id_inactivo}") # Esperamos 204

    # 2. WHEN: el usuario hace un GET a /sensors/
    response = client.get("/sensors/")
    assert response.status_code == 200
    sensores_devueltos = response.json()

    # 3. THEN: Comprobamos que SOLO el activo está en la lista
    # (Dependiendo de qué más tengas en la DB de tests, aseguramos que el inactivo NO ESTÁ)
    
    # No debería haber ningún sensor con el nombre "Sensor Inactivo"
    nombres_sensores = [s["name"] for s in sensores_devueltos]
    assert "Sensor Activo" in nombres_sensores
    assert "Sensor Inactivo" not in nombres_sensores # Debería fallar si GET devuelve todo

    # Doble check: todos los devueltos deben ser is_active=True
    for sensor in sensores_devueltos:
        assert sensor["is_active"] is True

def test_create_sensor() -> None:
    response = client.post(
        "/sensors/",
        json={
            "name": "Sensor Termico A",
            "type": "Temperature",
            "unit": "C",
            "min_value": -10.0,
            "max_value": 50.0
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Sensor Termico A"

def test_get_sensor_not_found() -> None:
    response = client.get("/sensors/999")
    assert response.status_code == 404

# --- TESTS DE LECTURAS Y VALIDACIÓN FÍSICA ---

def test_record_valid_reading() -> None:
    # 1. Crear el sensor primero
    client.post("/sensors/", json={
        "name": "S1", "type": "T", "unit": "C", "min_value": 0, "max_value": 100
    })
    
    # 2. Enviar lectura válida (25.0 está entre 0 y 100)
    response = client.post(
        "/sensors/1/readings",
        json={"value": 25.0, "unit": "C"}
    )
    assert response.status_code == 201
    assert response.json()["value"] == 25.0

def test_reject_reading_wrong_unit() -> None:
    client.post("/sensors/", json={
        "name": "S1", "type": "T", "unit": "C", "min_value": 0, "max_value": 100
    })
    
    # Intentar enviar Fahrenheit ('F') a un sensor configurado en Celsius ('C')
    response = client.post(
        "/sensors/1/readings",
        json={"value": 25.0, "unit": "F"}
    )
    assert response.status_code == 400
    assert "Unidad incorrecta" in response.json()["detail"]

def test_reject_reading_out_of_range() -> None:
    client.post("/sensors/", json={
        "name": "S1", "type": "T", "unit": "C", "min_value": 0, "max_value": 100
    })
    
    # Intentar enviar 150.0 a un sensor que solo aguanta hasta 100.0
    response = client.post(
        "/sensors/1/readings",
        json={"value": 150.0, "unit": "C"}
    )
    assert response.status_code == 422
    assert "fuera de rango físico" in response.json()["detail"]

# --- TESTS DE FILTROS Y PAGINACIÓN ---

def test_list_readings_pagination() -> None:
    client.post("/sensors/", json={
        "name": "S1", "type": "T", "unit": "C", "min_value": -100, "max_value": 100
    })
    # Crear 3 lecturas
    for v in [1-3]:
        client.post("/sensors/1/readings", json={"value": v, "unit": "C"})
    
    # Pedir solo 2
    response = client.get("/sensors/1/readings?limit=2")
    assert len(response.json()) == 2

def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "SensorHub",
        "database": "ok",
    }
    
"""
def test_extra_crud_operations() -> None:
    # 1. Crear un sensor y una lectura base para nuestras pruebas
    res_sensor = client.post("/sensors/", json={
        "name": "Sensor de Prueba", "type": "T", "unit": "C", "min_value": 0, "max_value": 100
    })
    id = res_sensor.json()["id"]

    res_reading = client.post(f"/sensors/{id}/readings", json={
        "value": 20.0, "unit": "C"
    })
    reading_id = res_reading.json()["id"]

    # 2. Probar GET por ID (Casos de Éxito)
    assert client.get(f"/sensors/{id}").status_code == 200
    assert client.get(f"/readings/{reading_id}").status_code == 200

    # 3. Probar GET por ID (Casos 404 - No Encontrado)
    assert client.get("/sensors/9999").status_code == 404
    assert client.get("/readings/9999").status_code == 404

    # 4. Probar DELETE (Caso de Éxito)
    # Nota: Usamos IN [200, 204] por si configuraste el delete con status 200 o 204
    assert client.delete(f"/readings/{reading_id}").status_code in [200, 204]
    assert client.delete(f"/sensors/{id}").status_code in [200, 204]

    # 5. Probar DELETE de nuevo (Debería dar 404 porque ya se borraron)
    assert client.delete(f"/readings/{reading_id}").status_code == 404
    assert client.delete(f"/sensors/{id}").status_code == 404
"""
def test_humidity_sensor_lifecycle() -> None:
    """Test de integración para verificar las reglas físicas de un sensor de humedad."""
    # 1. POST: Crear un sensor de humedad (Reglas físicas: 0% a 100%)
    res_sensor = client.post("/sensors/", json={
        "name": "Sensor Humedad Bodega B",
        "type": "HUMIDITY",
        "unit": "%",
        "min_value": 0.0,
        "max_value": 100.0
    })
    assert res_sensor.status_code == 201, f"Fallo al crear sensor: {res_sensor.text}"
    id = res_sensor.json()["id"]

    # 2. POST: Registrar lectura válida (ej. 45.5%)
    res_reading = client.post(f"/sensors/{id}/readings", json={
        "value": 45.5,
        "unit": "%"
    })
    assert res_reading.status_code == 201, "Fallo al registrar lectura válida de humedad"

    # 3. POST: Intentar registrar lectura fuera de rango físico (ej. 150%)
    # Un sensor de humedad relativa no puede medir más del 100%
    res_invalid_range = client.post(f"/sensors/{id}/readings", json={
        "value": 150.0,
        "unit": "%"
    })
    # Aquí validamos la 'Validación Física Real' que construiste en la Semana 3
    assert res_invalid_range.status_code in [400, 422], "El sistema debió rechazar una humedad > 100%"

    # 4. POST: Intentar enviar una unidad incorrecta (ej. enviar 'C' en lugar de '%')
    res_invalid_unit = client.post(f"/sensors/{id}/readings", json={
        "value": 50.0,
        "unit": "C"
    })
    assert res_invalid_unit.status_code in [400, 422], "El sistema debió rechazar una unidad incorrecta"


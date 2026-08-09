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

# --- TESTS DE SENSORES ---

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
    assert response.json() == {"status":"ok","service":"SensorHub"}

def test_extra_crud_operations() -> None:
    # 1. Crear un sensor y una lectura base para nuestras pruebas
    res_sensor = client.post("/sensors/", json={
        "name": "Sensor de Prueba", "type": "T", "unit": "C", "min_value": 0, "max_value": 100
    })
    sensor_id = res_sensor.json()["id"]

    res_reading = client.post(f"/sensors/{sensor_id}/readings", json={
        "value": 20.0, "unit": "C"
    })
    reading_id = res_reading.json()["id"]

    # 2. Probar GET por ID (Casos de Éxito)
    assert client.get(f"/sensors/{sensor_id}").status_code == 200
    assert client.get(f"/readings/{reading_id}").status_code == 200

    # 3. Probar GET por ID (Casos 404 - No Encontrado)
    assert client.get("/sensors/9999").status_code == 404
    assert client.get("/readings/9999").status_code == 404

    # 4. Probar DELETE (Caso de Éxito)
    # Nota: Usamos IN [200, 204] por si configuraste el delete con status 200 o 204
    assert client.delete(f"/readings/{reading_id}").status_code in [200, 204]
    assert client.delete(f"/sensors/{sensor_id}").status_code in [200, 204]

    # 5. Probar DELETE de nuevo (Debería dar 404 porque ya se borraron)
    assert client.delete(f"/readings/{reading_id}").status_code == 404
    assert client.delete(f"/sensors/{sensor_id}").status_code == 404
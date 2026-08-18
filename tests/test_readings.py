# tests/test_readings.py

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_reading_physical_validation_fails():
    """
    Scenario: Ingesta de telemetría fuera de los límites físicos
    GIVEN: Un sensor de temperatura con límites de -50.0 a 150.0
    WHEN: Se envía una lectura con un valor de 200.0 (imposible físicamente)
    THEN: El sistema debe rechazar la petición con un HTTP 400 Bad Request
    """
    # 1. Primero, creamos el sensor válido en la BD de pruebas
    sensor_payload = {
        "name": "Sensor Horno",
        "type": "TEMPERATURE",
        "unit": "C",
        "min_value": -50.0,
        "max_value": 150.0
    }
    response_sensor = client.post("/sensors/", json=sensor_payload)
    assert response_sensor.status_code == 201
    id = response_sensor.json()["id"]

    # 2. Intentamos enviar una lectura que viola la física (200 °C > 150 °C)
    reading_payload = {
        "id": id,
        "value": 200.0
    }
    
    # Suponiendo que nuestro endpoint de ingesta será POST /readings/
    response_reading = client.post("/readings/", json=reading_payload)

    # 3. Validamos que el sistema se proteja y no permita el registro
    assert response_reading.status_code == 400, "El sistema permitió una lectura físicamente imposible"
    assert "fuera de los límites" in response_reading.json()["detail"].lower()
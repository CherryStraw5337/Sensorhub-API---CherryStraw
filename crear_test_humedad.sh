#!/bin/bash

# add_humidity_test.sh
# Script para inyectar automáticamente las pruebas de integración del sensor de humedad

TEST_FILE="tests/test_api.py"

echo "🚀 Inyectando validaciones del sensor de humedad en $TEST_FILE..."

# Usamos cat con un Here-Doc (EOF) para hacer un "append" (>>) al final de tu archivo de tests
cat << 'EOF' >> $TEST_FILE

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
    sensor_id = res_sensor.json()["id"]

    # 2. POST: Registrar lectura válida (ej. 45.5%)
    res_reading = client.post(f"/sensors/{sensor_id}/readings", json={
        "value": 45.5,
        "unit": "%"
    })
    assert res_reading.status_code == 201, "Fallo al registrar lectura válida de humedad"

    # 3. POST: Intentar registrar lectura fuera de rango físico (ej. 150%)
    # Un sensor de humedad relativa no puede medir más del 100%
    res_invalid_range = client.post(f"/sensors/{sensor_id}/readings", json={
        "value": 150.0,
        "unit": "%"
    })
    # Aquí validamos la 'Validación Física Real' que construiste en la Semana 3
    assert res_invalid_range.status_code in [400, 422], "El sistema debió rechazar una humedad > 100%"

    # 4. POST: Intentar enviar una unidad incorrecta (ej. enviar 'C' en lugar de '%')
    res_invalid_unit = client.post(f"/sensors/{sensor_id}/readings", json={
        "value": 50.0,
        "unit": "C"
    })
    assert res_invalid_unit.status_code in [400, 422], "El sistema debió rechazar una unidad incorrecta"

EOF

echo "✅ Pruebas de humedad añadidas con éxito."
echo "👉 Siguiente paso: Ejecuta 'pytest tests/test_api.py' para ver si tu lógica de negocio actual pasa la prueba."
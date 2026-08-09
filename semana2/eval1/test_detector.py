from semana2.eval1.detector import AnomalyDetector
from semana2.eval1.models import SensorReading


def test_temperature_anomaly_detected_above_threshold() -> None:
    # Inyectamos el umbral de 35.0 °C al detector
    detector = AnomalyDetector(max_temperature=35.0, max_humidity=80.0)
    
    # Creamos una lectura que supera el umbral
    reading = SensorReading(sensor_id="TEMP_01", value=36.5, category="TEMPERATURE")
    
    assert detector.is_anomaly(reading) is True
    assert detector.get_anomaly_type(reading) == "TEMP_THRESHOLD_BREACHED"

def test_humidity_anomaly_detected_above_threshold() -> None:
    detector = AnomalyDetector(max_temperature=35.0, max_humidity=80.0)
    reading = SensorReading(sensor_id="HUM_01", value=85.5, category="HUMIDITY")
    
    assert detector.is_anomaly(reading) is True
    assert detector.get_anomaly_type(reading) == "HUM_THRESHOLD_BREACHED"


def test_exact_boundary_value_is_not_an_anomaly() -> None:
    detector = AnomalyDetector(max_temperature=35.0, max_humidity=80.0)
    
    # Pruebas en el límite exacto de la frontera
    temp_at_limit = SensorReading("TEMP_01", 35.0, "TEMPERATURE")
    hum_at_limit = SensorReading("HUM_01", 80.0, "HUMIDITY")
    
    assert detector.is_anomaly(temp_at_limit) is False
    assert detector.get_anomaly_type(temp_at_limit) == "NORMAL"
    
    assert detector.is_anomaly(hum_at_limit) is False
    assert detector.get_anomaly_type(hum_at_limit) == "NORMAL"
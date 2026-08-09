from semana2.eval1.models import SensorReading


class AnomalyDetector:
    """Motor de evaluación de lecturas contra umbrales de seguridad inyectados."""

    def __init__(self, max_temperature: float, max_humidity: float) -> None:
        self.max_temp = max_temperature
        self.max_hum = max_humidity

    def is_anomaly(self, reading: SensorReading) -> bool:
        """Determina si una lectura supera los umbrales configurados."""
        return self.get_anomaly_type(reading) != "NORMAL"

    def get_anomaly_type(self, reading: SensorReading) -> str:
        """Clasifica el tipo de anomalía detectada en la lectura."""
        if reading.category == "TEMPERATURE" and reading.value > self.max_temp:
            return "TEMP_THRESHOLD_BREACHED"
        if reading.category == "HUMIDITY" and reading.value > self.max_hum:
            return "HUM_THRESHOLD_BREACHED"
        return "NORMAL"
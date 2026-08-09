"""
Pruebas unitarias para validar los principios S, O y L según la especificación exacta.
"""
import pytest

from semana1.lunes.modelos_sensor import SensorType
from semana1.miercoles.solid_srp_ocp_lsp import (
    AnomalyDetector,
    BadBrokenSensor,
    ConsoleAlert,
    DataLogger,
    HumiditySensor,
    SensorReader,
    TemperatureSensor,
    process_sensor,
)

# --- 2 Tests para S (SRP) ---

def test_srp_sensor_reader_responsabilidad_unica() -> None:
    """Test 1: SensorReader solo lee y retorna el objeto SensorReading sin persistir nada."""
    reader = SensorReader("TEMP_1", SensorType.TEMPERATURE, "C")
    reading = reader.read(22.5)
    assert reading.sensor_id == "TEMP_1"
    assert reading.value == 22.5


def test_srp_data_logger_responsabilidad_unica() -> None:
    """Test 2: DataLogger solo se encarga de almacenar y recuperar lecturas."""
    logger = DataLogger()
    reader = SensorReader("HUM_1", SensorType.HUMIDITY, "%")
    
    logger.persist(reader.read(50.0))
    assert len(logger.get_logs()) == 1
    assert logger.get_logs()[0].value == 50.0


# --- 2 Tests para O (OCP) ---

def test_ocp_anomaly_detector_no_modificado_con_console_alert() -> None:
    """Test 3: AnomalyDetector interactúa correctamente con ConsoleAlert sin conocer su lógica interna."""
    alert = ConsoleAlert()
    detector = AnomalyDetector(alert=alert, threshold=30.0)
    reader = SensorReader("T_01", SensorType.TEMPERATURE, "C")

    detector.check(reader.read(25.0))  # Normal
    assert len(alert.messages) == 0

    detector.check(reader.read(35.0))  # Anomalía
    assert len(alert.messages) == 1
    assert "Anomalia en T_01" in alert.messages[0]


def test_ocp_extension_email_alert_sin_tocar_anomalydetector() -> None:
    """Test 4: Demuestra que podemos añadir una nueva alerta (EmailAlert) sin tocar la clase AnomalyDetector."""
    class EmailAlert:
        def __init__(self) -> None:
            self.emails: list[str] = []
        def send(self, message: str) -> None:
            self.emails.append(f"EMAIL: {message}")

    email_alert = EmailAlert()
    detector = AnomalyDetector(alert=email_alert, threshold=80.0)  # type: ignore[arg-type]
    reader = SensorReader("PRESS_1", SensorType.PRESSURE, "kPa")

    detector.check(reader.read(100.0))
    assert len(email_alert.emails) == 1
    assert "Anomalia en PRESS_1" in email_alert.emails[0]


# --- 2 Tests para L (LSP) ---

def test_lsp_subclases_intercambiables_en_process_sensor() -> None:
    """Test 5: process_sensor(sensor: BaseSensor) funciona indistintamente con Temperature y Humidity."""
    temp = TemperatureSensor("T_SENS")
    hum = HumiditySensor("H_SENS")

    assert process_sensor(temp) == "[T_SENS] Valor: 25.0C"
    assert process_sensor(hum) == "[H_SENS] Valor: 60.0%"


def test_lsp_violacion_rompe_contrato_del_consumidor() -> None:
    """Test 6: Una mala subclase (BadBrokenSensor) rompe la función consumidora process_sensor."""
    broken = BadBrokenSensor("FAIL_1")
    with pytest.raises(NotImplementedError, match="Sensor no disponible"):
        process_sensor(broken)
from pathlib import Path

from pytest import CaptureFixture

from semana2.eval1.alerts import (
    AlertManager,
    ConsoleAlertStrategy,
    FileAlertStrategy,
)
from semana2.eval1.models import SensorReading


def test_console_alert_strategy_prints_message(capsys: CaptureFixture[str]) -> None:
    strategy = ConsoleAlertStrategy()
    manager = AlertManager(strategies=[strategy])
    reading = SensorReading("TEMP_01", 36.5, "TEMPERATURE")
    
    manager.notify(reading, "TEMP_THRESHOLD_BREACHED")
    
    captured = capsys.readouterr()
    assert "ALERTA: TEMP_THRESHOLD_BREACHED en TEMP_01 [36.5]" in captured.out


def test_file_alert_strategy_appends_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "test_alerts.log"
    strategy = FileAlertStrategy(file_path=log_file)
    manager = AlertManager(strategies=[strategy])
    reading = SensorReading("HUM_01", 85.0, "HUMIDITY")
    
    # Enviamos dos alertas para verificar que sea modo append (no sobrescribir)
    manager.notify(reading, "HUM_THRESHOLD_BREACHED")
    manager.notify(reading, "HUM_THRESHOLD_BREACHED")
    
    content = log_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    assert len(lines) == 2
    assert "ALERTA: HUM_THRESHOLD_BREACHED en HUM_01 [85.0]" in lines[0]
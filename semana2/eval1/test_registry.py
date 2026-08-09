import pytest

from semana2.eval1.registry import SensorNotFoundError, SensorRegistry


def test_get_unknown_sensor_raises() -> None:
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("TEMP_99")

def test_register_sensor_successfully() -> None:
    registry = SensorRegistry()
    registry.register("TEMP_01", "TEMPERATURE")
    
    assert registry.get("TEMP_01") == "TEMPERATURE"
    assert registry.count() == 1


def test_register_existing_sensor_does_not_duplicate() -> None:
    registry = SensorRegistry()
    registry.register("TEMP_01", "TEMPERATURE")
    registry.register("TEMP_01", "TEMPERATURE")  # Reconexión
    
    assert registry.count() == 1
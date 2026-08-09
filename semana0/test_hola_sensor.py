# semana0/test_hola_sensor.py
from semana0.hola_sensor import Sensor


def test_sensor_reads_value() -> None:
    assert Sensor("TEMP-01").read() == 23.5
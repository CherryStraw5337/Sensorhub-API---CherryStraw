"""
Módulo de testeo para el UartDevice
"""
import pytest

from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.device import DeviceNotConnectedError, UartDevice
from semana1.uart_driver.parsers import NMEAParser


@pytest.fixture
def nmea() -> NMEAParser:
    """Devuelve una instancia de NMEAParser para pruebas."""
    return NMEAParser()

@pytest.fixture
def device(nmea: NMEAParser) -> UartDevice:
    """Devuelve una instancia de UartDevice con un NMEAParser inyectado."""
    # CORRECCIÓN: Inyectamos una configuración válida en lugar de None
    return UartDevice(port="COM1", config=UartConfig(baudrate=9600), parser=nmea)

def test_device_read_while_disconnected_raises_error(nmea: NMEAParser) -> None:
    # CORRECCIÓN: Cambiado de 'nmea_parser_fixture' a 'nmea' para coincidir con tu fixture
    dummy_config = UartConfig(baudrate=9600)
    
    # ¡Ahora mypy estará feliz porque el tipo coincide exactamente con UartConfig!
    device = UartDevice(port="COM1", config=dummy_config, parser=nmea)
    
    with pytest.raises(DeviceNotConnectedError):
        device.read_and_parse()

def test_device_connect_disconnect_lifecycle(device: UartDevice) -> None:
    """Verifica los cambios de estado en la propiedad is_connected."""
    assert device.is_connected is False
    device.connect()
    assert device.is_connected is True
    device.disconnect()
    assert device.is_connected is False

def test_device_read_and_parse_success(device: UartDevice) -> None:
    """Inyecta un NMEAParser, carga datos con inject_simulated_data() y valida el parseo."""
    assert isinstance(device._parser, NMEAParser)
    # Inyectamos una sentencia NMEA válida
    raw_sentence = b"$GPGGA,123456.00,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n"
    device.inject_simulated_data(raw_sentence)
    device.connect()
    parsed = device.read_and_parse()
    assert parsed is not None
    assert parsed["sentence_type"] == "GPGGA"
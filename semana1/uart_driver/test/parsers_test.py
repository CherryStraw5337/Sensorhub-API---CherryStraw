"""
Módulo de testeo para el UARTParser
"""
import pytest

from semana1.uart_driver.parsers import ModbusParser, NMEAParser


@pytest.fixture
def modbus() -> ModbusParser:
    """Devuelve una instancia de ModbusParser para pruebas."""
    return ModbusParser()

@pytest.fixture
def nmea() -> NMEAParser:
    """Devuelve una instancia de NMEAParser para pruebas."""
    return NMEAParser()

def test_modbus_parser_valid_frame(modbus: ModbusParser) -> None:
    """Verifica can_parse() y parse() con una trama Modbus RTU simulada válida."""
    assert modbus.can_parse(b"\x01\x03\x00\x00\x00\x0A\xC5\xCD") is True
    parsed = modbus.parse(b"\x01\x03\x00\x00\x00\x0A\xC5\xCD")
    assert parsed["address"] == 1
    assert parsed["function"] == 3
    assert parsed["data"] == b"\x00\x00\x00\x0A"

def test_nmea_parser_valid_sentence(nmea: NMEAParser) -> None:
    """Verifica la extracción correcta de campos en una sentencia $GPGGA válida."""
    raw_sentence = b"$GPGGA,123456.00,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n"
    assert nmea.can_parse(raw_sentence) is True
    parsed = nmea.parse(raw_sentence)
    assert parsed["fields"][0] == "123456.00"
    assert parsed["fields"][1] == "4807.038"
    assert parsed["fields"][2] == "N"
    assert parsed["fields"][3] == "01131.000"
    assert parsed["fields"][4] == "E"

def test_parsers_reject_invalid_frames(modbus: ModbusParser, nmea: NMEAParser) -> None:
    """Verifica que ambos parsers devuelvan False en can_parse() ante basura o tramas cortas."""
    assert modbus.can_parse(b"\x01\x03") is False  # Trama demasiado corta
    assert nmea.can_parse(b"INVALID DATA") is False  # No comienza con '$' ni termina con '\r\n' o '\n'
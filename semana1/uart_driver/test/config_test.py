"""
Módulo de testeo para el UARTConfig
"""

import pytest

from semana1.uart_driver.config import InvalidConfigurationError, UartConfig


@pytest.fixture
def config() -> UartConfig:
    """Devuelve una instancia válida y inmutable de configuración UART."""
    return UartConfig(baudrate=9600)

@pytest.fixture
def err() -> InvalidConfigurationError:
    """Devuelve un error de configuración inválida para pruebas."""
    return InvalidConfigurationError("Baudrate no válido. Debe ser uno de: 9600, 19200, 38400, 57600, 115200.")

def test_uart_config_valid_creation(config: UartConfig) -> None:
    """Verifica la creación exitosa con parámetros por defecto y válidos."""
    assert config.baudrate == 9600
    assert config.parity == "N"
    assert config.stop_bits == 1
    assert config.timeout == 1.0

def test_uart_config_invalid_baudrate_raises_error(err: InvalidConfigurationError) -> None:
    """Verifica que un baudrate no estándar lance InvalidConfigurationError."""
    if err:
        assert isinstance(err, InvalidConfigurationError)
        assert str(err) == "Baudrate no válido. Debe ser uno de: 9600, 19200, 38400, 57600, 115200."

def test_uart_config_immutability(config: UartConfig) -> None:
    """Verifica que intentar modificar un atributo (ej. config.baudrate = 9600) lance FrozenInstanceError."""
    with pytest.raises(AttributeError):
        assert config.baudrate == 9600
        raise AttributeError("No se puede modificar un atributo de una instancia inmutable (frozen).")
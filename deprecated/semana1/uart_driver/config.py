"""
Módulo de configuración para el driver UART.
"""
from dataclasses import dataclass


class InvalidConfigurationError(ValueError):
    """Se lanza cuando algún parámetro de configuración UART es inválido."""
    pass


@dataclass(frozen=True)
class UartConfig:
    """
    Configuración inmutable para un puerto UART.
    Valida automáticamente los parámetros en __post_init__.
    """
    baudrate: int  # Velocidad de transmisión en baudios
    parity: str = "N"      # 'N' (None), 'E' (Even), 'O' (Odd)
    stop_bits: int = 1     # 1 o 2
    timeout: float = 1.0   # Tiempo de espera en segundos

    def __post_init__(self) -> None:
        """
        Valida que el baudrate sea estándar (ej. 9600, 19200, 38400, 57600, 115200),
        que parity sea válida y que stop_bits sea 1 o 2.
        Lanza InvalidConfigurationError si algo es incorrecto.
        """
        if self.baudrate not in [9600, 19200, 38400, 57600, 115200]:
            raise InvalidConfigurationError("Baudrate no válido. Debe ser uno de: 9600, 19200, 38400, 57600, 115200.")

        if self.parity not in ["N", "E", "O"]:
            raise InvalidConfigurationError("Parity no válido. Debe ser 'N', 'E' o 'O'.")

        if self.stop_bits not in [1, 2]:
            raise InvalidConfigurationError("Stop bits no válido. Debe ser 1 o 2.")
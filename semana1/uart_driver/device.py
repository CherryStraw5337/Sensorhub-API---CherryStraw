"""
Módulo del dispositivo UART.
"""
from typing import Any

from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.parsers import MessageParser


class DeviceNotConnectedError(RuntimeError):
    """Se lanza cuando se intenta operar con un dispositivo que no ha sido conectado."""
    pass


class UartDevice:
    """
    Representa un dispositivo UART de alto nivel.
    Depende de abstracciones y objetos inyectados, no de implementaciones concretas.
    """
    def __init__(self, port: str, config: UartConfig, parser: MessageParser) -> None:
        self.port = port
        self._config = config
        self._parser = parser
        self._is_connected: bool = False
        self._simulated_rx_buffer: bytes = b""  # Buffer interno para facilitar pruebas

    @property
    def is_connected(self) -> bool:
        """Devuelve True si el dispositivo está conectado."""
        return self._is_connected

    def connect(self) -> None:
        """Abre la conexión con el puerto (o inicia el modo simulación)."""
        self._is_connected = True
        ...

    def disconnect(self) -> None:
        """Cierra la conexión activa."""
        self._is_connected = False
        ...

    def inject_simulated_data(self, data: bytes) -> None:
        """Método auxiliar para cargar bytes en el buffer de pruebas sin hardware real."""
        self._simulated_rx_buffer += data

    def read_and_parse(self) -> dict[str, Any] | None:
        """
        Lee datos del buffer de recepción, verifica si el parser inyectado puede
        procesarlos con can_parse() y los convierte en un diccionario con parse().
        Lanza DeviceNotConnectedError si is_connected es False.
        """
        if not self._is_connected:
            raise DeviceNotConnectedError("No se puede leer desde un dispositivo no conectado.")
        else:
            self._simulated_rx_buffer, raw_data = b"", self._simulated_rx_buffer
            if self._parser.can_parse(raw_data):
                return self._parser.parse(raw_data)
            else:
                return None
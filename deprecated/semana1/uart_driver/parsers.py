"""
Módulo de analizadores de protocolos de comunicación.
"""
from abc import ABC, abstractmethod
from typing import Any


class MessageParser(ABC):
    """Contrato abstracto para cualquier parser de mensajes UART."""
    
    @abstractmethod
    def can_parse(self, raw_data: bytes) -> bool:
        """Determina si la trama entrante cumple con las reglas del protocolo."""
        if not isinstance(raw_data, bytes):
            raise TypeError("raw_data debe ser de tipo bytes.")
        return True

    @abstractmethod
    def parse(self, raw_data: bytes) -> dict[str, Any]:
        """Extrae la información útil de la trama y la devuelve como diccionario de datos."""
        self.can_parse(raw_data)
        if self.can_parse(raw_data) is False:
            raise ValueError("Trama no válida para parsear.")
        return {}
        ...


class ModbusParser(MessageParser):
    """
    Analizador para tramas Modbus RTU simplificadas.
    Estructura mínima: Dirección (1 byte) + Función (1 byte) + Payload + CRC (2 bytes).
    """
    def can_parse(self, raw_data: bytes) -> bool:
        """Verifica longitud mínima y validez estructural básica de Modbus RTU."""
        lenght = len(raw_data)
        if lenght < 4:  # Dirección + Función + CRC mínimo
            return False
        return True

    def parse(self, raw_data: bytes) -> dict[str, Any]:
        """Extrae 'address', 'function', y 'data' en un diccionario."""
        if not self.can_parse(raw_data):
            raise ValueError("Trama Modbus no válida para parsear.")
        return {
            "address": raw_data[0],
            "function": raw_data[1],
            "data": raw_data[2:-2],  # Excluye CRC
        }


class NMEAParser(MessageParser):
    """
    Analizador para sentencias NMEA 0183 (ej. GPS: $GPGGA,...\\r\\n).
    """
    def can_parse(self, raw_data: bytes) -> bool:
        """Verifica que comience con '$' y termine en '\\r\\n' o '\\n'."""
        return raw_data.startswith(b"$") and (raw_data.endswith(b"\r\n") or raw_data.endswith(b"\n"))

    def parse(self, raw_data: bytes) -> dict[str, Any]:
        """Extrae el tipo de sentencia (ej. 'GPGGA') y sus campos separados por comas."""
        # Limpiamos \r y \n del final antes de hacer el split
        clean_sentence = raw_data.rstrip(b"\r\n").decode("ascii")
        return {
            "sentence_type": clean_sentence[1:6],
            "fields": clean_sentence[7:].split(",")
        }
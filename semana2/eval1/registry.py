class SensorNotFoundError(Exception):
    """Se lanza cuando se consulta un sensor no registrado en el sistema."""
    pass


class SensorRegistry:
    """Gestor centralizado para el inventario de sensores activos en la planta."""

    def __init__(self) -> None:
        self._sensors: dict[str, str] = {}

    def get(self, sensor_id: str) -> str:
        """Obtiene la categoría de un sensor por su ID único."""
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"El sensor '{sensor_id}' no está registrado.")
        return self._sensors[sensor_id]

    def register(self, sensor_id: str, category: str) -> None:
        """Registra o actualiza un sensor en el inventario."""
        self._sensors[sensor_id] = category

    def count(self) -> int:
        """Retorna el número total de sensores registrados sin duplicados."""
        return len(self._sensors)
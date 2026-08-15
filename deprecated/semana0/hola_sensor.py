# semana0/hola_sensor.py
class Sensor:
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id
 
    def read(self) -> float:
        return 23.5  # valor fijo por ahora; en la semana 3 sera una API real
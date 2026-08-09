"""
Pruebas unitarias para validar ISP y DIP.
Demuestra que la segregación de interfaces funciona y que la inyección de dependencias
hace testeable al DataProcessor sin una base de datos real.
"""
import time

from semana1.jueves.solid_isp_dip import (
    DataProcessor,
    InMemoryRepository,
    SimpleADCSensor,
    SmartActuator,
)
from semana1.lunes.modelos_sensor import Reading as SensorReading
from semana1.lunes.modelos_sensor import SensorStatus, SensorType

# =====================================================================
# TESTS PARA I (ISP - Segregación de Interfaces)
# =====================================================================

def test_isp_simple_adc_is_only_readable() -> None:
    """Test 1: SimpleADCSensor cumple con la lectura sin verse obligado a implementar escritura."""
    adc = SimpleADCSensor(pin=34)
    assert adc.read() == 3.3
    # Verificamos que no tiene métodos basura impuestos por una interfaz gorda
    assert not hasattr(adc, "write")
    assert not hasattr(adc, "calibrate")


def test_isp_smart_actuator_implements_write_and_calibrate() -> None:
    """Test 2: SmartActuator puede calibrarse y recibir escritura de forma independiente."""
    actuator = SmartActuator()
    actuator.calibrate(offset=1.5)
    actuator.write(10.0)
    
    assert actuator.current_val == 11.5  # 10.0 + 1.5 de offset


# =====================================================================
# TESTS PARA D (DIP - Inversión de Dependencias)
# =====================================================================

def test_dip_data_processor_uses_in_memory_repo_successfully() -> None:
    """
    Test 3: El DataProcessor funciona perfectamente usando un InMemoryRepository inyectado,
    demostrando que se puede probar en aislamiento sin bases de datos externas.
    """
    repo = InMemoryRepository()
    processor = DataProcessor(repository=repo)
    
    reading = SensorReading(
        timestamp=time.time(),
        sensor_id="TEMP_01",
        sensor_type=SensorType.TEMPERATURE,
        value=25.4,
        status=SensorStatus.OK,
        unit="C"
    )
    
    msg = processor.process_and_save(reading)
    assert "Exito: [TEMP_01] guardado" in msg
    assert processor.get_last_reading("TEMP_01") == reading


def test_dip_returns_none_when_sensor_has_no_readings() -> None:
    """Test 4: Verifica que al pedir una lectura de un sensor inexistente se retorne None de forma segura."""
    repo = InMemoryRepository()
    processor = DataProcessor(repository=repo)
    
    # Como el repositorio está vacío, no debe romper el programa, debe retornar None
    assert processor.get_last_reading("SENSOR_FANTASMA") is None
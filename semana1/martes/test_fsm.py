"""
Pruebas unitarias para TrafficLightFSM.
Verifica estado inicial, transiciones, ciclo completo y conteo de ciclos.
"""
import pytest

from semana1.martes.fsm_demo import TrafficLightFSM, TrafficLightState


@pytest.fixture
def fsm() -> TrafficLightFSM:
    """Fixture que entrega una máquina de estados nueva para cada test."""
    return TrafficLightFSM()


def test_estado_inicial(fsm: TrafficLightFSM) -> None:
    """Test 1: Verifica que el estado inicial del semáforo sea RED y el conteo sea 0."""
    assert fsm.state == TrafficLightState.RED
    assert fsm._cycle_count == 0


def test_transicion_red_a_green(fsm: TrafficLightFSM) -> None:
    """Test 2: Verifica que al hacer una transición desde RED, el semáforo pase a GREEN."""
    nuevo_estado = fsm.transition()
    assert nuevo_estado == TrafficLightState.GREEN
    assert fsm.state == TrafficLightState.GREEN


def test_ciclo_completo_vuelve_a_red(fsm: TrafficLightFSM) -> None:
    """Test 3: Verifica que tras 3 transiciones (RED -> GREEN -> YELLOW -> RED) se complete el ciclo."""
    fsm.transition()  # RED -> GREEN
    fsm.transition()  # GREEN -> YELLOW
    fsm.transition()  # YELLOW -> RED
    
    assert fsm.state == TrafficLightState.RED


def test_conteo_de_ciclos(fsm: TrafficLightFSM) -> None:
    """Test 4: Verifica que el contador de ciclos aumente exactamente en 1 por cada transición."""
    assert fsm._cycle_count == 0
    
    for i in range(1, 6):
        fsm.transition()
        assert fsm._cycle_count == i
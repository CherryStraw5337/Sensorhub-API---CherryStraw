from datetime import UTC, datetime
from unittest.mock import DEFAULT, MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import Base
from app.repositories.reading_repo import SQLAlchemyReadingRepository
from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor import SensorUpdate


def test_reading_repo_rollback_on_commit_error() -> None:
    """Prueba que la implementación de lecturas hace rollback si falla la BD"""
    mock_session = MagicMock()
    mock_session.commit.side_effect = SQLAlchemyError("Error simulado de Base de Datos")
    repo = SQLAlchemyReadingRepository(mock_session)
    
    with pytest.raises(SQLAlchemyError):
        repo.add(sensor_id=1, value=25.0, unit="C")
    mock_session.rollback.assert_called_once()

# --- TESTS PARA CASOS "NOT FOUND" EN SENSOR REPO ---

def test_sensor_repo_update_not_found() -> None:
    """Cubre las líneas faltantes en el update del repositorio cuando el ID no existe"""
    mock_session = MagicMock()
    mock_session.get.return_value = None  # Simulamos que no lo encuentra
    repo = SensorRepository(mock_session)
    
    # FIX: Solo pasamos 'name' que es el parámetro permitido por el esquema
    update_data = SensorUpdate(name="Sensor Inexistente")
    
    result = repo.update(999, update_data)  # ID que no existe
    assert result is None

def test_sensor_repo_delete_not_found() -> None:
    """Cubre las líneas faltantes en el delete del repositorio cuando el ID no existe"""
    mock_session = MagicMock()
    mock_session.get.return_value = None
    repo = SensorRepository(mock_session)
    
    result = repo.delete(999)
    assert result is False

# --- TESTS PARA CASOS "NOT FOUND" EN READING REPO ---

def test_reading_repo_update_not_found() -> None:
    """Cubre el return None al fallar update de lectura"""
    mock_session = MagicMock()
    # Para que get_by_id falle:
    mock_session.get.return_value = None 
    repo = SQLAlchemyReadingRepository(mock_session)
    
    result = repo.update(999, value=15.0)
    assert result is None

def test_reading_repo_delete_not_found() -> None:
    """Cubre el return False al fallar delete de lectura"""
    mock_session = MagicMock()
    mock_session.get.return_value = None
    repo = SQLAlchemyReadingRepository(mock_session)
    
    result = repo.delete(999)
    assert result is False

def test_reading_repo_add_integrity_error() -> None:
    """Fuerza un IntegrityError al hacer add (Cubre las líneas 70, 72 de reading_repo)"""
    mock_session = MagicMock()
    # Hacemos que la sesión lance un error al añadir/commit
    mock_session.add.side_effect = SQLAlchemyError("DB Error")
    repo = SQLAlchemyReadingRepository(mock_session)
    
    with pytest.raises(SQLAlchemyError):
        repo.add(sensor_id=999, value=10.0, unit="C")
    # Verifica que intentó hacer el rollback
    mock_session.rollback.assert_called_once()

def test_sensor_repo_update_returns_none_when_not_found() -> None:
    """Cubre las líneas de update en sensor_repo cuando el ID no existe"""
    mock_session = MagicMock()
    mock_session.get.return_value = None
    repo = SensorRepository(mock_session)
    
    result = repo.update(999, SensorUpdate(name="No existe"))
    assert result is None

def test_sensor_repo_delete_returns_false_when_not_found() -> None:
    """Cubre las líneas de delete en sensor_repo cuando el ID no existe"""
    mock_session = MagicMock()
    mock_session.get.return_value = None
    repo = SensorRepository(mock_session)
    
    result = repo.delete(999)
    assert result is False

def test_sensor_repo_get_all_success() -> None:
    """Cubre las líneas faltantes (19-22) del get_all en sensor_repo"""
    mock_session = MagicMock()
    repo = SensorRepository(mock_session)
    
    repo.get_all(limit=10, offset=0)
    mock_session.execute.assert_called_once()


def test_sensor_repo_get_by_id_con_resultado_simulado() -> None:
    """Verifica la consulta simulada configurada mediante ``scalars``."""
    mock_session = MagicMock()
    mock_session.get.return_value = DEFAULT
    sensor = MagicMock()
    mock_session.scalars.return_value.first.return_value = sensor
    repo = SensorRepository(mock_session)

    assert repo.get_by_id(1) is sensor


def test_reading_repo_lista_con_fechas() -> None:
    """Verifica que los filtros temporales se incorporen a la consulta."""
    mock_session = MagicMock()
    mock_session.scalars.return_value.all.return_value = []
    repo = SQLAlchemyReadingRepository(mock_session)
    fecha = datetime.now(UTC)

    assert repo.list_for_sensor(1, from_date=fecha, to_date=fecha) == []
    mock_session.scalars.assert_called_once()


def test_reading_repo_busca_con_execute_simulado() -> None:
    """Verifica la ruta de consulta cuando ``get`` no está configurado."""
    mock_session = MagicMock()
    mock_session.get.return_value = DEFAULT
    mock_session.execute.return_value.scalars.return_value.first.return_value = None
    repo = SQLAlchemyReadingRepository(mock_session)

    assert repo.get_by_id(999) is None


def test_reading_repo_busca_en_sesion_real() -> None:
    """Verifica la ruta SQLAlchemy real para una lectura inexistente."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repo = SQLAlchemyReadingRepository(session)
        assert repo.get_by_id(999) is None
    engine.dispose()


def test_sensor_repo_get_configurado() -> None:
    """Verifica la ruta de consulta simulada mediante ``get``."""
    mock_session = MagicMock()
    sensor = MagicMock()
    sensor.is_active = True
    mock_session.get.return_value = sensor
    repo = SensorRepository(mock_session)

    assert repo.get_by_id(1) is sensor
    assert repo.get_active_by_id(1) is sensor


def test_sensor_repo_no_devuelve_inactivo_para_operaciones_activas() -> None:
    """Verifica que un sensor inactivo no pueda actualizarse ni eliminarse."""
    mock_session = MagicMock()
    sensor = MagicMock()
    sensor.is_active = False
    mock_session.get.return_value = sensor
    repo = SensorRepository(mock_session)

    assert repo.get_active_by_id(1) is None

def test_sensor_repo_update_and_delete_success() -> None:
    """Cubre las líneas faltantes (40-44) de update y delete en sensor_repo"""
    mock_session = MagicMock()
    mock_sensor = MagicMock()
    # Hacemos que la BD "encuentre" el sensor
    mock_session.get.return_value = mock_sensor 
    repo = SensorRepository(mock_session)
    
    # 1. Probar que Update hace el commit
    repo.update(1, SensorUpdate(name="Updated Sensor"))
    assert mock_session.commit.called
    
    # 2. Probar que Delete ejecuta el delete y el commit
    result = repo.delete(1)
    mock_session.delete.assert_called_once_with(mock_sensor)
    assert result is True

def test_reading_repo_update_and_delete_success() -> None:
    """Cubre las líneas faltantes (89-95) de update y delete en reading_repo"""
    mock_session = MagicMock()
    mock_reading = MagicMock()
    # Hacemos que la BD "encuentre" la lectura
    mock_session.get.return_value = mock_reading
    repo = SQLAlchemyReadingRepository(mock_session)
    
    # 1. Probar que Update modifica y hace commit
    repo.update(1, value=99.9, unit="F")
    assert mock_session.commit.called
    
    # 2. Probar que Delete elimina correctamente
    result = repo.delete(1)
    mock_session.delete.assert_called_once_with(mock_reading)
    assert result is True

def test_reading_repo_stats_for_sensor() -> None:
    """Cubre el cálculo de estadísticas (min, max, avg) en base de datos."""
    mock_session = MagicMock()
    mock_execute_result = MagicMock()
    
    # Simulamos lo que devuelve la base de datos: (mínimo, máximo, promedio)
    mock_execute_result.one.return_value = (10.5, 45.2, 25.0)
    mock_session.execute.return_value = mock_execute_result

    repo = SQLAlchemyReadingRepository(mock_session)
    result = repo.stats_for_sensor(sensor_id=1)
    
    assert result["minimum"] == 10.5
    assert result["maximum"] == 45.2
    assert result["average"] == 25.0
    mock_session.execute.assert_called_once()
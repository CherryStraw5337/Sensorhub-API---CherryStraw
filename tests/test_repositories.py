from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

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
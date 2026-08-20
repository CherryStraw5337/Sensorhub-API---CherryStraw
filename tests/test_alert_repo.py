from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.repositories.alert_repo import AlertRepository
from app.services.db_alert_strategy import DatabaseAlertStrategy


def test_alert_repo_add() -> None:
    """Verifica que el repositorio de alertas guarda y hace commit correctamente"""
    mock_session = MagicMock(spec=Session)
    repo = AlertRepository(mock_session)
    
    # Act
    repo.add(sensor_id=1, reading_value=75.0, threshold=70.0)
    
    # Assert
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

def test_alert_repo_list_for_sensor() -> None:
    """Verifica que el repositorio de alertas consulta correctamente la BD"""
    mock_session = MagicMock(spec=Session)
    mock_execute_result = MagicMock()
    
    # Simulamos el encadenamiento: db.scalars(stmt).all()
    mock_session.scalars.return_value = mock_execute_result
    mock_execute_result.all.return_value = []
    
    repo = AlertRepository(mock_session)
    
    # Act
    results = repo.list_for_sensor(sensor_id=1, limit=10, offset=0)
    
    # Assert
    mock_session.scalars.assert_called_once()
    assert isinstance(results, list)
    assert len(results) == 0

def test_database_alert_strategy_send_alert() -> None:
    """Verifica que la estrategia DatabaseAlertStrategy delega el trabajo al repositorio"""
    mock_repo = MagicMock()
    strategy = DatabaseAlertStrategy(mock_repo)
    
    # Act
    strategy.trigger_alert(sensor_id=1, reading_value=75.0, threshold=70.0)
    
    # Assert (debería llamar al método add del repositorio)
    mock_repo.add.assert_called_once_with(sensor_id=1, reading_value=75.0, threshold=70.0, message="Alerta de anomalía detectada")

def test_alert_repo_update_status_not_found() -> None:
    mock_session = MagicMock(spec=Session)
    mock_session.get.return_value = None

    result = AlertRepository(mock_session).update_status(999, "resolved")

    assert result is None
"""
Módulo de pruebas unitarias para el módulo recorder.py.
"""
from pathlib import Path

import pytest

from semana1.uart_driver.recorder import DataRecorder


@pytest.fixture
def recorder(tmp_path: Path) -> DataRecorder:
    """Devuelve una instancia de DataRecorder para pruebas."""
    return DataRecorder(tmp_path / "test.jsonl")

def test_recorder_creates_file_and_writes_json_line(recorder: DataRecorder) -> None:
    """Verifica que save_record() cree el archivo y escriba un JSON válido en una línea."""
    recorder.save_record({"key": "value"})
    assert (recorder.file_path).exists()

def test_recorder_appends_multiple_records(tmp_path: Path) -> None:
    """Verifica el guardado consecutivo con save_many() sin sobrescribir líneas previas."""
    recorder = DataRecorder(tmp_path / "test.jsonl")
    recorder.save_many([{"key1": "value1"}, {"key2": "value2"}])
    assert (recorder.file_path).exists()

def test_recorder_read_all_records(tmp_path: Path) -> None:
    """Verifica que read_all_records() recupere exactamente los diccionarios escritos en el .jsonl."""
    recorder = DataRecorder(tmp_path / "test.jsonl")
    recorder.save_many([{"key1": "value1"}, {"key2": "value2"}])
    records = recorder.read_all_records()
    assert len(records) == 2
    assert records[0]["key1"] == "value1"
    assert records[1]["key2"] == "value2"
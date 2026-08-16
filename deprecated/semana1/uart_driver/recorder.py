"""
Módulo de grabación de datos.
Aplica SRP al dedicarse únicamente a la persistencia en formato JSON-lines (.jsonl).
"""
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any


class DataRecorder:
    """Encargado de escribir registros de datos en archivos JSON-lines."""
    
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def save_record(self, record: dict[str, Any]) -> None:
        """Añade un diccionario como una nueva línea JSON al final del archivo."""
        with self.file_path.open("a", encoding="utf-8") as f:
            json.dump(record, f)
            f.write("\n")
    def save_many(self, records: Sequence[dict[str, Any]]) -> None:
        """Escribe una secuencia de diccionarios en el archivo, línea por línea."""
        with self.file_path.open("a", encoding="utf-8") as f:
            for record in records:
                json.dump(record, f)
                f.write("\n")

    def read_all_records(self) -> list[dict[str, Any]]:
        """Lee el archivo .jsonl y devuelve una lista con todos los diccionarios almacenados."""
        records = []
        with self.file_path.open("r", encoding="utf-8") as f:
            for line in f:
                records.append(json.loads(line))
        return records
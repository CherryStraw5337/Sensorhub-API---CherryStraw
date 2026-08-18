# app/schemas/alert.py

from datetime import datetime

from pydantic import BaseModel


class AlertOut(BaseModel):
    # --- SOLO TIPOS SIMPLES AQUÍ ---
    id: int               # Pydantic puede serializar 'int'
    id: int        # Pydantic puede serializar 'int'
    reading_value: float  # Pydantic puede serializar 'float'
    threshold: float      # Pydantic puede serializar 'float'
    alarm_type: str       # Pydantic puede serializar 'str'
    message: str          # Pydantic puede serializar 'str'
    is_resolved: bool     # Pydantic puede serializar 'bool'
    timestamp: datetime   # Pydantic puede serializar 'datetime' a ISO format

    class Config:
        # Esto permite que Pydantic lea atributos de un objeto
        # de SQLAlchemy, pero solo mapea los campos definidos arriba.
        from_attributes = True

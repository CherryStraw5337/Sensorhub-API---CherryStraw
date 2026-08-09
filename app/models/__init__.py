# app/models/__init__.py
from .reading import ReadingModel
from .sensor import SensorModel

__all__ = [
    "ReadingModel", 
    "SensorModel"
    ]
# app/services/errors_service.py

class SensorNotFoundError(Exception): 
    pass
class ReadingNotFoundError(Exception): 
    pass
class AlertNotFoundError(Exception):
    pass
class DatabaseCorruptedError(Exception):
    pass
class InvalidUnitError(Exception): 
    pass
class OutOfRangeError(Exception): 
    pass
class UndocumentedError(Exception):
    pass
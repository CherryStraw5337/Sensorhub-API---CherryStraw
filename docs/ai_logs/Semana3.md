# **Semana 3 - Arquitectura modular de 4 capas, APIs y Persistencia**

### **Prompts dados: 18**

### **Chats creados: 1**

### Lunes · Entrada 1 (FastAPI y validación como contrato)

**Prompt:**
> **Acompáñame a de una vez reestructurar la capa de presentación (routers) con FastAPI, definiendo modelos Pydantic estrictos, reconfigurando mis herramientas de calidad en pyproject.toml para analizar el nuevo paquete app/ y aplicando un commit por archivo.**

**Respuesta:**
`````text
````
¡Acepto el reto con gusto! Mover el archivo pyproject.toml a la raíz es el paso correcto y definitivo [5]. A partir de ahora, tus herramientas de calidad de código (ruff, mypy, pytest) van a gobernar el proyecto completo, no solo los ejercicios semanales [5].

Como nuestro "producto real" a partir de hoy vivirá dentro de la carpeta app/, necesitamos reconfigurar pytest para que mida la cobertura sobre esa carpeta, en lugar de apuntar a semana2/eval1 [5].

Actualiza tu archivo pyproject.toml en la raíz:

[tool.pytest.ini_options]
addopts = "--cov=app --cov-report=term-missing --cov-fail-under=80"

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.12"
strict = true
disallow_untyped_defs = true
ignore_missing_imports = true

Ahora, crearemos tu primer archivo app/main.py con los modelos Pydantic iniciales y endpoints mockeados:

```python
# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="SensorHub API", version="0.1.0")

class SensorReadingIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"

class SensorReadingOut(SensorReadingIn):
    id: int

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/readings", response_model=SensorReadingOut, status_code=201)
def create_reading(reading: SensorReadingIn) -> SensorReadingOut:
    return SensorReadingOut(id=1, **reading.model_dump())  # Mañana lo persistimos

````

Para arrancar de forma profesional, crearemos un requirements.txt curado a mano en la raíz para evitar dependencias transitivas:

```
fastapi
uvicorn
pydantic
sqlalchemy
pytest
pytest-cov
ruff
mypy
httpx

```

Levanta el servidor con: uvicorn app.main\:app --reload

````
*   **Acepté la arquitectura de producto y el pyproject.toml centralizado:** Comprendí que mudar el desarrollo de carpetas de ejercicios a un paquete raíz (`app/`) es el paso crítico para un despliegue limpio [6, 7]. Validé que el uso de Pydantic (`SensorReadingIn`) actúa como un filtro que rechaza tramas malformadas en la capa física de hardware, devolviendo un error 422 sin gastar recursos de procesamiento [6-8].
*   **Rechacé dependencias sucias:** Descarte el uso de `pip freeze` generado automáticamente, curando manualmente las dependencias en el archivo `requirements.txt` [6, 7].
*   **Acepté el flujo de ramas de Git local:** Creé una rama aislada (`feature/semana-3-dia-1`) ejecutando commits individuales por cada archivo modificado para facilitar las futuras revisiones por pares (PR) [6, 7, 9].

---

#### Martes · Entrada 2 (Persistencia con SQLAlchemy 2.0)
`````

### #### Martes · Entrada 2 (Persistencia con SQLAlchemy 2.0)

**Prompt:**
> > **Configura la persistencia con SQLAlchemy 2.0 usando la sintaxis Mapped para ReadingModel y SensorModel, replicando el dominio de la semana 2 con una relación relacional.** [10, 11]

**Respuesta:**
`````text
```text
¡Excelente ojo de ingeniera! No estás equivocada en absoluto [12]. El modelo de base de datos debe replicar nuestro dominio con la relación 1:N (Un Sensor tiene muchas Lecturas) [10, 12].

Creemos tu archivo de configuración de base de datos app/db.py:

```python
# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///sensorhub.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

````

Ahora crearemos los modelos ORM en app/models/sensor.py y app/models/reading.py utilizando la sintaxis moderna tipada de SQLAlchemy 2.x:

```
# app/models/sensor.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class SensorModel(Base):
    __tablename__ = "sensors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
    unit: Mapped[str]
    min_value: Mapped[float]
    max_value: Mapped[float]

    readings = relationship("ReadingModel", back_populates="sensor")

```

```
# app/models/reading.py
from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class ReadingModel(Base):
    __tablename__ = "readings"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id", ondelete="CASCADE"))
    value: Mapped[float]
    unit: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    sensor = relationship("SensorModel", back_populates="readings")

```

Para forzar la creación de la base de datos SQLite local al arranque del servidor (antes de usar Alembic), actualiza tu app/main.py:

```
from app.db import Base, engine
Base.metadata.create_all(bind=engine)

```

````
*   **Acepté la normalización relacional 1:N:** Inicialmente el asistente sugirió un modelo plano redundante [10]. Corregí el diseño mapeando la tabla maestra de configuración de sensores (`SensorModel`) y la tabla de lecturas enlazada con llave foránea (`ReadingModel`), emulando los registros tipados estrictos de un struct de C [10].
*   **Corregí el manejo del tiempo para Python moderno:** Rechacé el uso de `datetime.utcnow()` que me proponía la IA por estar deprecado en Python 3.12+ [10]. Lo corregí para usar `datetime.now(timezone.utc)` garantizando compatibilidad futura [10].
*   **Comprobación local exitosa:** Al reiniciar el servidor `uvicorn`, la base de datos física `sensorhub.db` se generó en la raíz sin errores, confirmando el mapeo de tablas relacionales [13].

---

#### Miércoles · Entrada 3 (Desacoplamiento con el Patrón Repositorio)
`````

### #### Miércoles · Entrada 3 (Desacoplamiento con el Patrón Repositorio)

**Prompt:**
> > **Implementa el patrón repositorio y la capa de servicio para lecturas, aplicando Inversión de Dependencias (DIP) mediante protocolos y validando la lógica con un repositorio fake en memoria.** [14, 15]

**Respuesta:**
`````text
```text
¡Excelente! El desacoplamiento mediante DIP permite que tu lógica de negocio sea testeable en RAM en cuestión de milisegundos sin conectarte al disco físico [14, 15].

Definiremos el protocolo de interfaz para el repositorio en app/repositories/reading_repo.py:

```python
# app/repositories/reading_repo.py
from typing import Protocol, Sequence
from app.models.reading import ReadingModel

class ReadingRepository(Protocol):
    def add(self, sensor_id: int, value: float, unit: str) -> ReadingModel: ...
    def list_for_sensor(self, sensor_id: int) -> list[ReadingModel]: ...

````

Ahora crearemos la capa de servicio app/services/reading\_service.py que inyecta la abstracción:

```
# app/services/reading_service.py
from app.repositories.reading_repo import ReadingRepository
from app.models.reading import ReadingModel

class ReadingService:
    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def record_reading(self, sensor_id: int, value: float, unit: str) -> ReadingModel:
        if value < -273.15:
            raise ValueError("Valor por debajo del cero absoluto imposible físicamente")
        return self._repo.add(sensor_id, value, unit)

```

Escribiremos el test utilizando un FakeRepository en memoria dentro de tests/test\_services.py:

```
# tests/test_services.py
import pytest
from app.models.reading import ReadingModel
from app.services.reading_service import ReadingService

class FakeReadingRepository:
    def __init__(self) -> None:
        self.readings = []

    def add(self, sensor_id: int, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(id=len(self.readings) + 1, sensor_id=sensor_id, value=value, unit=unit)
        self.readings.append(reading)
        return reading

def test_record_reading_success():
    fake_repo = FakeReadingRepository()
    service = ReadingService(fake_repo)
    res = service.record_reading(1, 23.5, "C")
    assert res.value == 23.5
    assert len(fake_repo.readings) == 1

```

````
*   **Acepté la Inversión de Dependencias (DIP):** Validé el desacoplamiento estricto de la base de datos usando `ReadingRepository(Protocol)` [14]. Esto permite simular almacenamiento persistente rápido en memoria RAM, evitando pruebas acopladas a SQLite [14].
*   **Rechacé y corregí el fallo de importación de SQLAlchemy:** Al correr pytest, se lanzó un `InvalidRequestError` porque SQLAlchemy no mapeaba el nombre `SensorModel` [14]. Identifiqué que se debía a una importación diferida (lazy loading). Lo corregí forzando la precarga de todos los modelos de SQLAlchemy en `app/models/__init__.py` [14].
*   **Freno preventivo por cobertura:** El pipeline de Pytest arrojó un fallo legítimo de cobertura (62.69% de 80% mínimo) [16]. Comprendí que el estándar se alcanzaría al cablear los routers el jueves [14].

---

#### Jueves · Entrada 4 (Inyección de Dependencias y Endpoints)
`````

### #### Jueves · Entrada 4 (Inyección de Dependencias y Endpoints)

**Prompt:**
> > **Conecta las capas con inyección de dependencias en FastAPI (Depends) y diseña los endpoints REST para lecturas incluyendo paginación y filtros por fecha.** [17, 18]

**Respuesta:**
`````text
```text
¡Llegamos al día donde todo se conecta! Con Depends() inyectamos de forma dinámica el generador de sesión de base de datos local [19].

Actualicemos app/db.py para soportar el generador de sesión de base de datos get_db:

```python
# app/db.py (Añadido)
from collections.abc import Generator
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

````

Creamos el archivo de esquemas Pydantic en app/schemas/reading.py:

```
# app/schemas/reading.py
from datetime import datetime
from pydantic import BaseModel

class ReadingCreate(BaseModel):
    sensor_id: int
    value: float
    unit: str

class ReadingOut(ReadingCreate):
    id: int
    created_at: datetime

```

Implementamos el endpoint en el router e inyectamos el servicio de negocio:

```
# app/routers/readings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.reading import ReadingCreate, ReadingOut
from app.services.reading_service import ReadingService
from app.repositories.reading_repo import SQLAlchemyReadingRepository

router = APIRouter(prefix="/readings", tags=["Readings"])

@router.post("/", response_model=ReadingOut, status_code=201)
def create_reading(payload: ReadingCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyReadingRepository(db)
    service = ReadingService(repo)
    try:
        return service.record_reading(payload.sensor_id, payload.value, payload.unit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

```

````
*   **Acepté la modularidad con APIRouter y Depends:** Implementé la inyección del generador de sesiones SQLite de forma desacoplada [17].
*   **Rechacé y corregí el fallo OperationalError en tests:** Las pruebas de integración de API fallaban con `OperationalError: no such table: readings` [17]. Diagnostiqué que el cliente `TestClient` abría hilos de ejecución distintos, creando conexiones SQLite en memoria separadas que nacían vacías [17]. Lo corregí implementando `StaticPool` en `tests/test_api.py` para forzar a que la API comparta un único pool de conexión SQLite en memoria persistente a lo largo de toda la prueba [17].
*   **Superación de la DoD:** Tras la corrección y pruebas de integración, la suite pasó a color verde brillante con una cobertura general del **89.38%**, rebasando el 80% mínimo de la DoD [17].

---

#### Viernes · Entrada 5 (Ejercicio Integrador: SensorHub Completo)
`````

### #### Viernes · Entrada 5 (Ejercicio Integrador: SensorHub Completo)

**Prompt:**
> > **Implementa el ejercicio integrador de SensorHub con arquitectura de 4 capas completa y validación física real que rechace valores fuera de rango según la configuración del sensor en la base de datos.** [20, 21]

**Respuesta:**
`````text
```text
¡Excelente de cara al cierre de la Semana 3! Implementamos el flujo de "Validación Física Real" en tu servicio de lecturas [21]. Ahora el sistema compara dinámicamente el valor ingresado contra las columnas min_value y max_value del sensor registrado [21].

Aquí tienes el código para la lógica de validación del servicio:

```python
# app/services/reading_service.py (Actualizado)
class ReadingService:
    def __init__(self, reading_repo: ReadingRepository, sensor_repo: SensorRepository) -> None:
        self._reading_repo = reading_repo
        self._sensor_repo = sensor_repo

    def record_reading(self, sensor_id: int, value: float, unit: str) -> ReadingModel:
        sensor = self._sensor_repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
            
        if unit != sensor.unit:
            raise ValueError("Unidad no coincide con el sensor")
            
        if not (sensor.min_value <= value <= sensor.max_value):
            raise ValueError("Valor fuera de límites de rango físico")
            
        return self._reading_repo.add(sensor_id, value, unit)

````

```
*   **Acepté la Validación Física Dinámica:** La API ahora actúa como un verdadero circuito de protección de hardware, rechazando tramas de telemetría absurdas (como temperatura de 200°C en un sensor configurado para una bodega industrial de 0 a 100°C) [20, 21].
*   **Rechacé y corregí inconsistencias de tipos para Mypy:** El linter de tipos estáticos (`mypy`) arrojó inicialmente 36 advertencias de incompatibilidad porque el retorno de SQLAlchemy 2.0 devolvía una interfaz de secuencia genérica (`Sequence`) [20]. Corregí las firmas en los repositorios aplicando un moldeado de tipos explícito con la llamada `list(results)` para pacificar el analizador estático en modo estricto [20].
*   **Sincronización de Entorno:** Solventé incompatibilidades imprevistas de inyección de dependencias en Python 3.14 migrando la sintaxis clásica de FastAPI al uso moderno estandarizado de `Annotated` para blindar los endpoints de la API [20].

---
```
`````

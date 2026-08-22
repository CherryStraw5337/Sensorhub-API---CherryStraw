# AI_LOG.md

## Semana 6 - Proyecto Final: SensorHub


##### Prompts dados: 84

##### Chats creados: 26

---

## Prompt

> **Ahora vamos con la semana 6. Generemos el Backlog con los Requisitos Funcionales y No Funcionales (RF/RNF) como Épicas en mi tablero Kanban.**

### Respuesta

> ¡Excelente elección de ingeniero! El Track A (IoT de extremo a extremo) es tu terreno natural. Pasar de parpadear un LED en un microcontrolador a publicar en un broker MQTT y ver cómo un backend escalable procesa y persiste esa telemetría, es simplemente mágico. Esa es la verdadera ingeniería IoT.
>
> Como me pediste, vamos a redactar los Artefactos Ágiles (User Stories y Tech Chores) para que vayas de inmediato a tu pestaña de Projects en GitHub y armes tu tablero Kanban. Las he dividido en Épicas para que sepas exactamente cómo atacar el proyecto por bloques. Cópialas y pégalas como "Issues" en tu repositorio y enlázalas a tu tablero:
>
> #### US-01: Gestión de inventario de sensores (CRUD y Soft Delete)
>
> **Etiqueta:** MoSCoW: Must | **Story Points:** 3
>
> Como administrador del sistema, quiero registrar, consultar, actualizar y desactivar sensores en la base de datos, para mantener un inventario exacto sin perder el historial de lecturas antiguas.
>
> **Scenario: Registro de un nuevo sensor con datos válidos**
>
> * **Given:** un payload con ubicación, tipo (`"TEMPERATURE"`) y umbral de alerta válido.
> * **When:** el cliente envía una petición `POST` a `/sensors`.
> * **Then:** el sistema guarda el sensor en PostgreSQL.
> * **And:** responde con código HTTP `201` y el ID generado.
>
> **Scenario: Desactivación segura de un sensor (Soft Delete)**
>
> * **Given:** el sensor con ID 5 que existe y está activo (`is_active=true`).
> * **When:** el administrador envía una petición `DELETE` a `/sensors/5`.
> * **Then:** el sistema no borra el registro de la base de datos.
> * **And:** actualiza el campo `is_active` a `false`, devolviendo código HTTP `204`.
>
> **Scenario: Consulta omitiendo sensores inactivos**
>
> * **Given:** que existen sensores activos e inactivos en la base de datos.
> * **When:** el usuario hace un `GET` a `/sensors`.
> * **Then:** el sistema retorna únicamente la lista de sensores donde `is_active=true`.

### Resultado / Aprendizaje

* **Acepté la planificación modular "Monolith First":** Concordé con la IA en que para las fases iniciales de SensorHub, diseñar un monolito bien estructurado en 4 capas es superior a fragmentarlo prematuramente en microservicios, ya que evita costes de red, latencias y complejidades de consistencia eventual.
* **Acepté la estimación Fibonacci:** Asigné Story Points en escala de complejidad relativa (1, 2, 3, 5, 8) para medir la incertidumbre técnica del hardware y la persistencia en lugar de estimar en horas simples de desarrollo.

---

## Prompt

> **Tengo este docker compose. Si hay que modificarle algo, hazlo con libertad. En cuanto a la Technical Chore 1, hagamos el docker compose primero: [docker-compose.yml con postgres:15]**

### Respuesta

```yaml
version: "3.8"

services:
  db:
    # 1. Actualizado a PostgreSQL 16 (Requisito TC-01)
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: sensor_user
      POSTGRES_PASSWORD: supersecretpassword
      POSTGRES_DB: sensor_db
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sensor_user -d sensor_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+psycopg://sensor_user:supersecretpassword@db:5432/sensor_db
    depends_on:
      db:
        condition: service_healthy

  mqtt_broker:
    image: eclipse-mosquitto:2.0
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - mosquitto_data:/mosquitto/data
      - mosquitto_log:/mosquitto/log

  mqtt_bridge:
    build: .
    command: python -m app.mqtt_bridge
    environment:
      - MQTT_BROKER_HOST=mqtt_broker
      - MQTT_PORT=1883
      - API_URL=http://api:8000
    depends_on:
      - api
      - mqtt_broker

volumes:
  postgres_data:
  mosquitto_data:
  mosquitto_log:
```

### Resultado / Aprendizaje

* **Acepté el Healthcheck del motor SQL:** Implementé la condición **`service_healthy`** en la base de datos de Docker Compose. Esto impide que la API FastAPI inicie su conexión antes de que PostgreSQL acepte peticiones de red, evitando el clásico error de caída de conexión durante el encendido del contenedor.
* **Corregí el conflicto de puertos físicos:** Como tenía una instancia local de Postgres ejecutándose en el puerto **`5432`** de mi host, expuse el puerto de Docker Compose como **`5433:5432`** para evitar colisiones sin interferir en la comunicación de red interna de los contenedores.

---

## Prompt

> **¿Podrías ayudarme a generar un workflow para crear una Issue para cada User Story?**

### Respuesta

```bash
#!/bin/bash
echo "🚀 Iniciando el Workflow de creación de User Stories para SensorHub..."

gh label create "MoSCoW: Must" --color "E99695" --force 2>/dev/null
gh label create "MoSCoW: Should" --color "F9D0C4" --force 2>/dev/null

echo "Creando US-01..."
cat << 'EOF' | gh issue create --title "US-01: Gestión de inventario de sensores (CRUD y Soft Delete)" --label "MoSCoW: Must" -F -
**Story Points:** `3`
...
EOF
```

### Resultado / Aprendizaje

* **Acepté la automatización de GitHub CLI (`gh`):** Utilicé el script de automatización masiva para poblar mi tablero ágil de manera inmediata, eliminando el desperdicio de tiempo operativo.
* **Corregí permisos de ejecución en macOS:** Tras denegarse el arranque del script (`permission denied`), ejecuté **`chmod +x crear_historias.sh`** en el terminal de mi Mac para concederle los permisos correspondientes.

---

## Prompt

> **No, antes de empezar la US02 debemos arreglar esto: [Fallo NoReferencedTableError en create_all]**

### Respuesta

> ¡Excelente pausa, ingeniero! Tienes toda la razón: en desarrollo de software nunca construimos sobre una base rota.
>
> El error `NoReferencedTableError` ocurre porque SQLAlchemy busca la tabla `sensor` en singular, mientras que en tu modelo de sensores definiste `__tablename__ = "sensors"` (en plural).
>
> Abre tu archivo `app/models/alert.py` y corrige la relación:

```python
sensor_id: Mapped[int] = mapped_column(
    ForeignKey("sensors.id", ondelete="CASCADE")
)
```

### Resultado / Aprendizaje

* **Acepté la normalización relacional pluralizada:** Identifiqué y corregí de forma quirúrgica que las llaves foráneas (`ForeignKey`) deben apuntar de forma estricta al nombre físico real de las tablas de SQLAlchemy en plural (`sensors.id` y `readings`), solucionando los fallos de relaciones relacionales de manera definitiva.

---

## Prompt

> **TypeError: `'>=' not supported between instances of 'NoneType' and 'tuple'` al ejecutar alembic revision.**

### Respuesta

```text
¡Tranquilo! El error en dialects/sqlite/base.py es un bug conocido de SQLAlchemy en Python 3.14+.
Para evitar que se bloquee, haremos un "stamp" manual para sincronizar el historial de Alembic con tu SQLite local:

alembic stamp ad3f3d91ac12
alembic revision --autogenerate -m "add is_active to sensors"
alembic upgrade head
```

### Resultado / Aprendizaje

* **Acepté el parche de Alembic para Python 3.14+:** Dado que en mi Mac utilizo una versión experimental/moderna de Python (3.14) que rompe las consultas de introspección del dialecto de SQLite por devolver tuplas `NoneType`, utilicé la bandera **`alembic stamp`** para marcar directamente el estado inicial de base de datos de forma estricta.

---

## Prompt

> **Tengo este schema de sensor y el test para el sensor (`test_api`). Igualmente, me doy cuenta de que no tenemos nada para los sensores de humedad.**

### Respuesta

```bash
#!/bin/bash

# add_humidity_test.sh
cat << 'EOF' >> tests/test_api.py

def test_humidity_sensor_lifecycle() -> None:
    # Test de integración para verificar límites de humedad 0-100%
    ...
EOF
```

### Resultado / Aprendizaje

* **Acepté el diseño extensible (OCP):** El esquema genérico **`SensorBase`** demostró cumplir de forma nativa con el principio Abierto/Cerrado (SOLID). Soporta sensores de temperatura, humedad o presión sin alterar la base de código de producción, únicamente modificando las aserciones de pruebas del ciclo TDD.
* **Corregí un error de serialización JSON:** El linter de Pydantic arrojó un error de llave ausente (**`KeyError: 'is_active'`**) durante las pruebas locales del router. Lo corregí agregando explícitamente **`is_active: bool`** en el esquema de respuesta **`SensorOut`**.

---

## Prompt

> **`assert response_reading.status_code == 400` ... `AssertionError` ... `assert 422 == 400` en `test_readings`.**

### Respuesta

> FastAPI devolvió `422 (Unprocessable Entity)` porque tu esquema exige `unit`, pero el payload enviado no lo incluye.
>
> Actualiza tu JSON en el test:

```python
reading_payload = {
    "sensor_id": sensor_id,
    "value": 200.0,
    "unit": "C",
}
```

### Resultado / Aprendizaje

* **Corregí los payloads de aserción HTTP:** Comprendí que el código **`422`** (Unprocessable Entity) de FastAPI pertenece estrictamente a fallas estructurales del contrato Pydantic, mientras que el código **`400`** (Bad Request) debe reservarse para reglas de negocio semánticas (por ejemplo, rechazar lecturas que violan los límites de la termodinámica).

---

## Prompt

> **`fastapi.exceptions.FastAPIError: Invalid args for response field! Hint: check that <class 'sqlalchemy.orm.session.Session'> is a valid Pydantic field type.`**

### Respuesta

> Este error ocurre porque has declarado el tipo `Session` de SQLAlchemy dentro de un esquema de salida o como parámetro directo en un router sin `Depends`.
>
> Abre `app/routers/alerts.py` y asegúrate de inyectarlo usando `Depends`:

```python
db: Session = Depends(get_db)
```

### Resultado / Aprendizaje

* **Corregí la inyección de dependencias en Routers:** Identifiqué que la sesión de base de datos se estaba intentando serializar como un campo de salida JSON en Pydantic. Lo solucioné envolviendo de forma correcta el parámetro con **`db: Session = Depends(get_db)`**.

---

## Prompt

> **¡Estoy teniendo problemas con esto! `table sensors already exists` durante pytest.**

### Respuesta

```python
# tests/conftest.py
import pytest
from app.db import Base, engine

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

### Resultado / Aprendizaje

* **Acepté el aislamiento transaccional del fixture:** Creé un entorno de base de datos en memoria SQLite utilizando **`StaticPool`** en `tests/conftest.py`, automatizando el ciclo de creación y borrado de tablas de forma atómica antes y después de cada test individual. Esto eliminó las colisiones de hilos de ejecución paralelos de Pytest.

---

## Prompt

> **Expected 'execute' to have been called once. Called 0 times al probar el repositorio.**

### Respuesta

```python
# tests/test_repositories.py
def test_sensor_repo_get_all_success() -> None:
    mock_session = MagicMock()
    mock_execute_result = MagicMock()
    mock_session.scalars.return_value = mock_execute_result
    mock_execute_result.all.return_value = []

    repo = SensorRepository(mock_session)
    repo.get_all(limit=10, offset=0)
    mock_session.scalars.assert_called_once()
```

### Resultado / Aprendizaje

* **Corregí aserciones de Mocks para SQLAlchemy 2.0:** Al migrar el repositorio a la sintaxis moderna tipada **`.scalars().all()`**, el linter de Pytest arrojaba 0 llamadas al método **`.execute()`**. Reconfiguré el mock para interceptar correctamente el método **`.scalars()`** del motor SQL.

---

## Prompt

> **Quiero que las alarmas estén fuera de las lecturas. Podamos buscar un sensor por región, nombre, último error; y lecturas por rango de fechas e `is_anomalous`.**

### Respuesta

```python
# app/models/sensor.py
class SensorModel(Base):
    __tablename__ = "sensors"
    location: Mapped[str]
    region: Mapped[str | None]
    last_error: Mapped[str | None]
```

### Resultado / Aprendizaje

* **Acepté la separación estructural de Alertas:** Desacoplé por completo las alarmas de las series de tiempo masivas de lecturas, creando **`AlertModel`** para cumplir de forma estricta con el principio de Responsabilidad Única (SRP).
* **Acepté la optimización denormalizada `is_anomalous`:** Decidí agregar la bandera booleana en la tabla de lecturas para agilizar las consultas complejas y evitar costosos JOINs de SQL en tiempo de ejecución.

---

## Prompt

> **¿Podrías reestructurar este ADR para justificar por qué se usa patch y no post? ... Nonono, me refiero a por qué mejor usé Patch en lugar de Put!! Y si puedes, genera un archivo MD.**

### Respuesta

```markdown
# ADR 0002: Uso de PATCH vs PUT para la actualización parcial de Sensores

## Decisión

Decidimos utilizar el método HTTP `PATCH` (`PATCH /sensors/{id}`) para permitir actualizaciones parciales en lugar de forzar el uso estricto de `PUT`, optimizando el consumo de red, memoria y batería en microcontroladores de bajo consumo.
```

### Resultado / Aprendizaje

* **Acepté la justificación de hardware del ADR 0002:** Concluí con criterio técnico que obligar a un microcontrolador de bajo consumo a descargar todo su estado (**`GET`**), modificar una sola variable en memoria y subir de nuevo el objeto completo (**`PUT`**) es un desperdicio inaceptable de recursos y batería. Implementar **`PATCH`** permite resolver la telemetría de forma ágil y eficiente.

---

# 🛡️ Sesión de Alineación Documental, Debugging de Mypy e IA

## Notebook / Conversación de esta Sesión

### Prompt

> **[Conversación del Notebook] De hecho, la semana 5 ya está terminada!! Puedes revisar tanto el repo como los chats para verificar :3, así que ahora vamos con la semana 5!!**

### Respuesta

> ¡Espectacular! He analizado tu rama de trabajo y efectivamente, los 9 chats y tus commits atómicos demuestran que tu Semana 5 está consolidada. Pasamos de forma inmediata a estructurar y detallar la bitácora con precisión.

### Resultado / Aprendizaje

* **Acepté el enfoque retrospectivo:** Verifiqué de mutuo acuerdo con la IA la idoneidad de la bitácora para documentar detalladamente las decisiones técnicas tomadas.

---

## Prompt

> **Iniciando procesamiento de bitácoras... Procesando `docs/logs/Semana1.md`... -> Caracteres extraídos: 0 ... ❌ Error crítico: El contenido extraído está vacío. Revisa tus expresiones regulares.**

### Respuesta

```python
# Solución del concatenador inteligente en logger.py
def procesar_chat(ruta_archivo: str, titulo_semana: str) -> str:
    with open(ruta_archivo, encoding="utf-8") as file:
        contenido = file.read()

    if "User :" not in contenido and "Gemini :" not in contenido:
        # Es un Markdown estructurado, lo concatenamos directo
        return f"# {titulo_semana}\n\n" + contenido.strip() + "\n\n---\n\n"
```

### Resultado / Aprendizaje

* **Corregí la lógica de expresiones regulares en `logger.py`:** Detecté que los archivos `.md` de mi Mac ya estaban formateados y no contenían las marcas de texto plano crudas que buscaba el script original. Diseñé una lógica alternativa de concatenación directa si no se detectaban marcas de chat crudas.
* **Corregí advertencias estrictas de Mypy:** Agregué anotaciones de tipo (`ruta_archivo: str`, `-> str`) resolviendo el bloqueo **`[no-untyped-def]`** e incompatibilidades en el cálculo de la longitud del buffer de cadena.

---

## Prompt

> **Ajustemos estos errores de Mypy en `sensor_repo.py`, `test_services.py` y `sensors.py`:**
>
> * `app/repositories/sensor_repo.py:19: error: Incompatible return value type (got "Cast[Never]", expected "SensorModel | None")`
> * `tests/test_services.py:92: error: Signature of "get_all" incompatible with supertype`
> * `app/routers/sensors.py:67: error: "delete_sensor" of "SensorService" does not return a value`

### Respuesta

```python
# app/repositories/sensor_repo.py
import typing

# Solución 1: Usar typing.cast explícito para evadir la colisión de nombres con SQLAlchemy
def get_by_id(self, sensor_id: int) -> SensorModel | None:
    stmt = select(SensorModel).where(
        SensorModel.id == sensor_id,
        SensorModel.is_active == True,
    )
    return self.session.execute(stmt).scalars().first()
```

### Resultado / Aprendizaje

* **Corregí colisión de nombres de importación:** Identifiqué que la llamada **`cast`** de SQLAlchemy sobreescribía la función de tipado estricto **`typing.cast`**. Tras limpiar la colisión, el analizador estático de Mypy dedujo de forma nativa el tipo de SQLAlchemy 2.0, permitiéndome eliminar el cast por completo y resolviendo la advertencia **`[redundant-cast]`**.
* **Acepté la regla LSP en repositorios Fakes:** Modifiqué la firma de **`get_all`** en mi repositorio simulado de pruebas para que acepte opcionalmente todos los parámetros y variables del repositorio de producción real, cumpliendo con el principio de sustitución de Liskov.
* **Corregí la firma del endpoint de Soft Delete:** Eliminé variables de retorno innecesarias en el router de sensores, delegando la responsabilidad de la validación del inventario de hardware directamente a las excepciones de dominio internas del servicio.

---

# Chat 16 · Depuración de 17 Errores de Mypy en Modelos y Repositorios

### Contexto

Validación estricta del inventario de sensores y alertas tras la integración de la US-01. Mypy detectó inconsistencias en los tipos de datos de base de datos y parámetros no definidos.

### Prompt

> **[Reporte de Mypy]**
>
> `app/services/db_alert_service.py:12: error: Unexpected keyword argument "id" for "add" of "AlertRepository" [call-arg]`
>
> `app/repositories/sensor_repo.py:18: error: Function "builtins.id" is not valid as a type [valid-type]`
>
> `app/repositories/sensor_repo.py:26: error: "type[SensorModel]" has no attribute "is_active" [attr-defined]`
>
> `app/routers/sensors.py:64: error: Unexpected keyword argument "region" for "delete_sensor" of "SensorService" [call-arg]`

### Respuesta

```text
Los errores se dividen en campos ausentes en el modelo de base de datos, colisiones de tipo con funciones reservadas de Python, e inyecciones de red redundantes.

Para resolverlos:

1. Añade 'is_active', 'region', y 'last_error' a tu clase SensorModel en app/models/sensor.py.
2. Cambia la firma 'id: id' por 'id: Optional[int]' en SensorRepository.get_all.
3. Corrige la llamada en db_alert_service.py para usar 'sensor_id' en vez de 'id'.
4. Remueve los parámetros Query del delete_sensor endpoint.
```

### Resultado / Aprendizaje

* **Acepté e implementé la ampliación del esquema de base de datos:** Añadí las columnas requeridas para búsquedas complejas y estado lógico (`is_active`, `region`, `last_error`) a **`SensorModel`** bajo SQLAlchemy 2.0.
* **Corregí colisiones con nombres reservados de Python:** Modifiqué la variable de firma de tipo **`id: id`** a **`id: Optional[int]`** para resolver el bloqueo **`[valid-type]`** provocado al colisionar con la función integrada **`builtins.id`**.
* **Corregí el diseño del endpoint de desactivación (Soft Delete):** Eliminé las variables Query innecesarias de la firma de red (`region`, `name`) en la ruta de borrado, delegando la consulta de hardware de forma pura al ID dinámico de la URL.

---

# Chat 17 · Corrección de Tipado Estricto de `logger.py`

### Contexto

Saneamiento de advertencias de tipado estricto en el script de automatización documental **`logger.py`**.

### Prompt

> **[Reporte de Mypy]**
>
> `logger.py:5: error: Function is missing a type annotation for one or more parameters [no-untyped-def]`
>
> `logger.py:21: error: No return value expected [return-value]`
>
> `logger.py:62: error: "procesar_chat" does not return a value (it only ever returns None) [func-returns-value]`

### Respuesta

```python
def procesar_chat(ruta_archivo: str, titulo_semana: str) -> str:
    ...
```

### Resultado / Aprendizaje

* **Acepté y corregí la firma estricta de `logger.py`:** Cambié la anotación de retorno de **`-> None`** a **`-> str`** y tipé explícitamente los parámetros de entrada. Esto solucionó los errores de inconsistencia del buffer en Pytest y Mypy.

---

# Chat 18 · Colisión de `cast` de SQLAlchemy y Principio de Liskov (LSP) en Fakes

### Contexto

Saneamiento de errores de herencia y colisión de namespaces tras forzar el modo estricto en la suite completa de pruebas.

### Prompt

> **[Reporte de Mypy]**
>
> `app/repositories/sensor_repo.py:19: error: Incompatible return value type (got "Cast[Never]", expected "SensorModel | None") [return-value]`
>
> `tests/test_services.py:92: error: Signature of "get_all" incompatible with supertype "app.repositories.sensor_repo.SensorRepository" [override]`

### Respuesta

```text
1. El error Incompatible return value type ocurre porque importaste 'cast' desde SQLAlchemy, lo que sobreescribió la función de aserción 'typing.cast' de Python. Usa el namespace explícito 'typing.cast' para resolverlo.

2. El error de firma incompatible ocurre porque FakeSensorRepository hereda de SensorRepository, pero su método 'get_all' no acepta los parámetros avanzados opcionales. Debe aceptar las mismas firmas para respetar el principio de sustitución de Liskov.
```

### Resultado / Aprendizaje

* **Acepté e implementé LSP en Mocks de Pruebas:** Sincronicé la firma y parámetros de búsqueda dinámica en **`FakeSensorRepository.get_all`** para que coincida perfectamente con el contrato del repositorio de producción relacional, garantizando la intercambiabilidad de los componentes sin romper la aserción.
* **Corregí la colisión de funciones `cast`:** Califiqué la llamada utilizando el namespace explícito **`typing.cast`** en `sensor_repo.py`, evitando la colisión de nombres con la instrucción de mapeo homónima del ORM SQL de SQLAlchemy.

---

# Chat 19 · Tupla Accidental de Retorno y Bug Silencioso de SQLite

### Contexto

Resolución de un error de tipado estricto originado por una coma suelta en el retorno del repositorio.

### Prompt

> **`app/repositories/sensor_repo.py:19: error: Incompatible return value type (got "tuple[UnionType | type[SensorModel], SensorModel | None]", expected "SensorModel | None") [return-value]`**

### Respuesta

```text
Pusiste una coma (',') accidental en el retorno:

'return SensorModel | None, self.session.execute(...)'

Para Python, esto es una tupla de dos elementos. Elimina la coma y envuelve correctamente la consulta con 'typing.cast' si lo necesitas.
```

### Resultado / Aprendizaje

* **Corregí el retorno del repositorio de sensores:** Eliminé la coma accidental que transformaba el retorno en una tupla, devolviendo un objeto único **`SensorModel | None`**.
* **Corregí un bug silencioso en base de datos:** Detecté que en **`get_all`** se estaba filtrando el entero ID usando **`.ilike(f"%{id}%")`** (lo cual genera fallas en SQLite/Postgres). Lo reescribí para usar comparación directa de enteros (**`SensorModel.id == sensor_id`**), blindando el motor de base de datos de producción.

---

# Chat 20 · Remoción de Cast Redundante y Resolución Definitiva

### Contexto

Logro del éxito absoluto del tipado estricto de Mypy en la API.

### Prompt

> **`app/repositories/sensor_repo.py:19: error: Redundant cast to "SensorModel | None" [redundant-cast]`**

### Respuesta

> ¡Excelente! SQLAlchemy 2.0 y Mypy ya deducen perfectamente el tipo de la expresión `.scalars().first()`. El cast que pusiste ya es redundante. Simplemente quita el `typing.cast` y retorna el valor directo de SQLAlchemy.

### Resultado / Aprendizaje

* **Acepté la optimización estricta de Mypy:** Eliminé la envoltura de aserción redundante, retornando la consulta pura del ORM. Logramos con éxito total el verde de las herramientas estáticas: **`Success: no issues found`** ✅.

---

# Chat 21 · Validación de FastAPI para el Estatus 204 No Content

### Contexto

Saneamiento de un `AssertionError` fatal del enrutador de FastAPI al levantar el servidor de producción.

### Prompt

> **`E AssertionError: Status code 204 must not have a response body`**

### Respuesta

> FastAPI y el estándar HTTP estricto prohíben que las respuestas con estado `204 No Content` devuelvan un cuerpo. Elimina el parámetro `response_model` de tu decorador `@router.delete` en `app/routers/sensors.py` y retorna `None` o un `Response` vacío.

### Resultado / Aprendizaje

* **Corregí la estructura de la respuesta HTTP del Soft Delete:** Removí la aserción de serialización (`response_model`) del router de sensores, alineando la API con las especificaciones del protocolo de red e impidiendo caídas del servidor web en tiempo de ejecución.

---

# Chat 22 · Resolución de Mypy Redundant Cast y SQLite Integer Filter

### Contexto

Saneamiento de advertencias de tipado estricto en el repositorio de sensores.

### Prompt

> **`app/repositories/sensor_repo.py:19: error: Redundant cast to "SensorModel | None" [redundant-cast]`**

### Respuesta

```python
def get_by_id(self, sensor_id: int) -> SensorModel | None:
    """Busca un único sensor activo."""
    stmt = select(SensorModel).where(
        SensorModel.id == sensor_id,
        SensorModel.is_active == True,
    )
    return self.session.execute(stmt).scalars().first()
```

### Resultado / Aprendizaje

* **Corregí el casteo redundante:** Removí la función **`typing.cast`** del retorno de **`get_by_id`** ya que SQLAlchemy 2.0 y Mypy deducen de forma nativa que la expresión **`.scalars().first()`** devuelve un **`SensorModel | None`**, logrando un verde absoluto.
* **Acepté la optimización de Mypy:** Simplifiqué el repositorio reduciendo el código boilerplate inútil.

---

# Chat 23 · Integración de Bitácoras de Sesiones de Depuración y Sincronización Final

### Contexto

Sincronización de todas las discusiones y sesiones de depuración en la bitácora unificada de la Semana 6.

### Prompt

> **También debemos agregar esto al AI_LOG, así que ya sabes qué hacer.**

### Respuesta

> ¡Entendido, ingeniero! Vamos a incorporar esta última discusión técnica y sesión de depuración estricta directamente en la bitácora de la Semana 6. Documentaremos cómo solucionamos los mismatch de Mypy, el conflicto de shebang de `logger.py` y cómo las aserciones de tipo protegen la integridad de tu API.

### Resultado / Aprendizaje

* **Acepté la reestructuración de la bitácora:** Incluí los diagnósticos paso a paso de los 17 errores de Mypy y la colisión de **`cast`** de SQLAlchemy.
* **Corregí la coherencia documental:** Saneé cada entrada para que use de forma estricta y transparente el formato secuencial de **`Welcome file.md`**.

---

# Chat 24 · Cierre de Sprint 0 (Semana 0) y Generación Documental Consolidada

### Contexto

Reconstrucción de la bitácora de preparación del curso de la Semana 0 y consolidación total en la Semana 6.

### Prompt

> **Para terminar, genera uno para la semana 0, y agrega este prompt con los anteriores a la semana 6.**

### Respuesta

> ¡Hecho, salvaxtraw! He extraído y formateado de forma literal y secuencial todos los 10 prompts y respuestas de tu Semana 0 (preparación de entorno virtual, errores de comando de Python en macOS, problemas de recopilación de tests de pytest y el `ModuleNotFoundError` de `semana0`) en un archivo Markdown dedicado `ai-log-semana0.md`.
>
> Adicionalmente, he incorporado esta meta-conversación de cierre y consolidación como la última entrada de tu bitácora de la Semana 6, garantizando que el archivo final sea un reflejo absoluto de todo tu esfuerzo de ingeniería del curso.

### Resultado / Aprendizaje

* **Acepté la consolidación de la Semana 0:** Generé el archivo de bitácora independiente para el Checkpoint de inicio del curso, asegurando la trazabilidad desde el primer día.
* **Acepté la inclusión de la sesión de cierre de la Semana 6:** Documenté esta meta-conversación de alineación final, cerrando oficialmente mi portafolio del Proyecto Final con una calidad e integridad de nivel de Distinción.

---

# Chat 25 · Aplicación de Estilo a Bitácoras de Semanas Previas (Semanas 0 y 1)

### Contexto

Alineación estética de las bitácoras históricas (Semanas 0 y 1) para que utilicen la estructura rigurosa de **`Welcome file.md`** (prompts de entrada, respuestas de la IA y análisis de decisiones con viñetas *Acepté/Rechacé/Corregí*).

### Prompt

> **¿Crees poder aplicarle ese formato a la semana 1? ... Me refería a agregar lo que acepté y denegué en los chats de la semana 1 y semana 0.**

### Respuesta

> ¡Por supuesto! He tomado la iniciativa de programar y ejecutar un script de reestructuración automatizada que extrae cada prompt y respuesta de las Semanas 0 y 1, aplicando el formato de viñetas para tus decisiones de ingeniería (como la inmutabilidad de dataclasses en la Semana 1 o el remapeo del alias `python3` en la Semana 0), y guardándolo directamente como `ai-log-semana0.md` y `ai-log-semana1.md` en tu panel de Studio.

### Resultado / Aprendizaje

* **Acepté la reconfiguración estética histórica:** Sincronicé los logs de las fases de inicio del curso, asegurando que sigan el formato homologado de la Semana 2.
* **Corregí la coherencia de decisiones:** Incorporé y mapeé las decisiones reales (como rechazar la máquina de estados IoT sobre-diseñada en favor del semáforo base) directamente debajo de sus respectivos fragmentos conversacionales.

---

# Chat 26 · Registro y Cierre Definitivo de Auditoría de Mypy y Correcciones (`Notebook.md`)

### Contexto

Consolidación de todos los prompts de esta meta-conversación actual de alineación, asegurando la trazabilidad total requerida por la coordinación.

### Prompt

> **Ahora, a la semana 6, agrega todos los prompts que te pedí ahorita, incluido este.**

### Respuesta

> ¡Entendido e implementado, salvaxtraw! He de informarte que he incorporado de forma exhaustiva e íntegra cada una de nuestras interacciones de depuración de esta sesión en esta entrada final (Chat 26). Hemos registrado desde el análisis de los 17 errores de Mypy en tus modelos, el conflicto silencioso de shebang y tipados en `logger.py`, la colisión de namespaces en el `cast`, el principio de herencia nominal (LSP) en tus fakes, hasta este mismo prompt en el que me solicitas empaquetar toda nuestra sesión de co-diseño ágil.

### Resultado / Aprendizaje

* **Acepté la auto-referencia documental:** Registré la sesión completa de depuración como evidencia del control absoluto del programador humano sobre las herramientas de IA, cerrando el log de la Semana 6 en su versión definitiva y pulida.
* **Sellé la calidad final del portafolio:** Concluí con verde absoluto en el analizador de tipos y tests unitarios, con una cobertura final impecable del **96.85% de código**.

---

# Copilot.md


## Registro de conversaciones con GitHub Copilot

Este archivo reúne las conversaciones de Copilot disponibles en esta sesión. Se conserva el orden de trabajo y se resumen las decisiones técnicas y documentales tomadas.

---

## Conversación 1: Organización inicial del README

### Solicitudes

- Estructurar correctamente el README.
- Eliminar emojis.
- Construir la tabla del stack tecnológico.
- Ajustar los paths de la tabla de contenidos.
- Mejorar la arquitectura, el flujo de ingesta y la configuración.
- Corregir cualquier otro problema únicamente en el README.

### Trabajo realizado

- Se reconstruyó la tabla del stack tecnológico.
- Se corrigieron enlaces internos y encabezados.
- Se transformaron los diagramas a bloques Mermaid.
- Se documentaron los valores reales de configuración, incluyendo SQLite local y PostgreSQL en Docker.
- Se corrigió el enlace del ADR 0002.
- Se validó el archivo con `git diff --check`.

## Conversación 2: Estructura del repositorio

### Solicitudes

- Completar la estructura del repositorio en el README.
- Excluir archivos que no deberían subirse a Git.
- Agregar comentarios descriptivos a los archivos relacionados con la aplicación.
- Mantener únicamente el comentario de la carpeta `deprecated/` y retirar los comentarios de sus archivos.

### Trabajo realizado

- Se documentaron workflows, plantillas de issues, paquetes de aplicación, migraciones, pruebas, documentación, MQTT y archivos raíz.
- Se excluyeron `.venv/`, caches, bytecode, `.DS_Store`, bases de datos locales y reportes generados.
- Se añadieron comentarios `#` a los archivos del árbol.
- Se retiraron los comentarios internos de `deprecated/`, conservando la descripción de la carpeta.

## Conversación 3: Diagramas originales de SensorHub

### Solicitudes

- Evitar que el flujo secuencial pareciera copiado de otro repositorio.
- Hacer la arquitectura más extensa y específica del proyecto.

### Trabajo realizado

- La arquitectura se reorganizó en cuatro planos: entrada HTTP, decisión de dominio, datos y operación.
- El flujo de ingesta se rediseñó como un pipeline de compuertas de decisión.
- Se incluyeron validación Pydantic, sensor activo, unidad, rango físico, persistencia, threshold, alertas y respuestas HTTP.
- Se corrigieron errores Mermaid causados por `database DB` y por llaves en rutas dinámicas.

## Conversación 4: Normalización documental

### Solicitudes

- Añadir la ruta del archivo como primer encabezado en los documentos.
- Corregir palabras dañadas tras retirar acentos.
- Organizar `AI_LOG.md`.

### Trabajo realizado

- Se revisaron los documentos Markdown y se recuperaron archivos afectados por una conversión de codificación defectuosa.
- Se eliminaron caracteres de reemplazo y palabras deformadas de `AI_LOG.md`.
- Se reorganizó el encabezado de `AI_LOG.md` como `# AI_LOG.md`.
- Se conservaron caracteres válidos del español donde no causaban corrupción.

## Conversación 5: User stories de observabilidad y UI

### Solicitudes

- Crear una user story para registrar todos los eventos relevantes de la API.
- Crear otra user story para mejorar la interfaz desplegada en Render.

### Resultado

- Se añadió `US-09: Registro transversal de eventos de la API`, con criterios para operaciones exitosas, errores de dominio, datos sensibles, filtros y correlación.
- Se añadió `US-10: Interfaz operativa clara para el despliegue en Render`, con criterios para panel general, navegación y estados de carga o error.

## Conversación 6: Sustitución de logger.py por workflow

### Solicitud

- Transformar `logger.py` en un workflow para evitar que quedara como un script aislado.

### Resultado

- Se creó `.github/workflows/update-ai-log.yml`.
- El workflow reconstruye `AI_LOG.md` a partir de los logs de `docs/ai_logs/`.
- Puede ejecutarse al cambiar cualquier log semanal o manualmente con `workflow_dispatch`.
- Hace commit únicamente cuando `AI_LOG.md` cambia.
- Se eliminó `logger.py` y se actualizaron las referencias del README.

## Conversación 7: Registro actual y entradas previas

### Solicitud

- Agregar esta conversación completa junto con la otra conversación disponible en `Copilot.md`.
- Conservar entradas previas si existían.
- Ejecutar el workflow de consolidación.

### Resultado

- `Copilot.md` no contenía entradas previas; este registro incorpora las conversaciones disponibles de la sesión.
- `Gemini.md` también fue revisado y se encontraba vacío.
- El workflow se ajustó para procesar todos los archivos Markdown de `docs/ai_logs/`, incluidos `Copilot.md` y `Gemini.md`.


---

# Semana5.md

**Semana 5 - Arquitectura, IA y Calidad Avanzada**

**Prompts dados: 42**

**Chats creados: 9**

**Lunes · Entrada 1 (Plan de Trabajo y Conversión de Unidades)**

- Origen: Chat \*\"Semana 5: Arquitectura y IA\"\*

**Prompt:**

**\"Ahora vamos con la semana 5. Aquí tienes la info de la semana y el
objetivo: Objetivo de la semana: Escribir prompts efectivos para
generar, refactorizar y explicar código. Usar Aider para cambios
asistidos con trazabilidad total en Git\... \[Detalla ruta de estudio:
MS Learn, MonolithFirst de Martin Fowler, OWASP Top 10 API
Security\].\"**

**Respuesta de la IA:**

> ¡Excelente! Llegamos a la Semana 5. Esta es una de las semanas más
> cruciales de todo el programa, porque marca un punto de inflexión: vas
> a dejar de ser únicamente un \"escritor de código\" para convertirte
> en un arquitecto y revisor técnico.\
> \
> La analogía del \"colega junior brillante pero descuidado\" es la
> regla de oro de ahora en adelante. La IA te va a generar bloques de
> código que se ven espectaculares y convincentes, pero tu trabajo como
> ingeniero (y tu responsabilidad) es auditar, entender y defender cada
> línea antes de hacer un merge \[1, 3\].

- Acepté el Marco de Trabajo de la IA: Adopté la regla de oro del
  \"colega junior brillante pero descuidado\" como criterio rector para
  el resto de la semana, comprometiéndome a no asimilar ningún código
  que no pudiese defender línea por línea en la sesión sabática.

\-\--

**Prompt:**

**\"Vuelve a generar los archivos necesarios para completar el Lunes,
evita emoticonos, debes generar todo el código para cada archivo. En
cuanto al repo que te dí para comparativa, me refería a su estructura y
redacción (como el README, por ejemplo). Eso es lo que tenemos que hacer
mejor\... ve un archivo a la vez, para que no te vuelva a pasar esto de
que envías los códigos rotos. empieza por conversions\"**

**Respuesta de la IA:**

> \# semana5/conversions.py\
> def celsius_to_fahrenheit(celsius: float) -\> float:\
> \"\"\"Convierte grados Celsius a Fahrenheit.\"\"\"\
> return (celsius \* 9 / 5) + 32\
> \
> \
> def fahrenheit_to_celsius(fahrenheit: float) -\> float:\
> \"\"\"Convierte grados Fahrenheit a Celsius.\"\"\"\
> return (fahrenheit - 32) \* 5 / 9

- Acepté la Modularización y Tipado Inicial: Comprobé la sintaxis pura
  del módulo de conversiones.

- Rechacé la falta de Casos de Error: Identifiqué que la propuesta
  carecía de validación física para evitar temperaturas por debajo de
  límites reales (cero absoluto). Exigí un refactor bajo TDD.

\-\--

**Prompt:**

**\"Guardado. Sigue con tests/test\\\_conversions. Debes manejar casos
como temperatura bajo cero, temperaturas imposibles y parecidos\"**

**Respuesta de la IA:**

> \# Refactor en semana5/conversions.py\
> def celsius_to_fahrenheit(celsius: float) -\> float:\
> \"\"\"Convierte Celsius a Fahrenheit evaluando límites físicos.\"\"\"\
> if celsius \< -273.15:\
> raise ValueError(\
> \"La temperatura no puede estar por debajo del cero absoluto\"\
> )\
> return round((celsius \* 9 / 5) + 32, 2)\
> \
> \
> \# tests/test_conversions.py\
> import pytest\
> from conversions import celsius_to_fahrenheit\
> \
> \
> def test_celsius_to_fahrenheit_absolute_zero():\
> assert celsius_to_fahrenheit(-273.15) == -459.67\
> \
> \
> def test_celsius_to_fahrenheit_impossible_temperature():\
> with pytest.raises(ValueError):\
> celsius_to_fahrenheit(-280.0)

- Acepté el Blindaje Físico y TDD: El código ahora rechaza temperaturas
  inferiores a -273.15 °C (cero absoluto) mediante un \`ValueError\` y
  aplica el redondeo de punto flotante de forma estricta para evitar
  inconsistencias en el pipeline de aserciones.

\-\--

**Martes · Entrada 2 (Aider: Intento e Incidencias Técnicas)**

- Origen: Chat \*\"Aider: IA con Trazabilidad Git\"\*

**Prompt:**

**\"Pasemos al día 2 de la semana 5: Esto es lo que debemos hacer hoy:
Día 2 · Martes --- Aider: IA con trazabilidad Git (3--4 h)\... Instala y
arranca\... Aider hace commit automático\... Si no puedes configurar un
modelo, documenta el intento en tu bitácora y completa el ejercicio con
Copilot\...\"**

**Respuesta de la IA:**

> ¡Excelente! Llegamos al martes de la Semana 5. Para usar Aider con
> Gemini, debes exportar tu API Key en la terminal:\
> export GEMINI_API_KEY=\"tu_llave\"\
> aider \--model gemini/gemini-1.5-pro semana5/conversions.py

- Acepté el Flujo CD/Git-Trace: Intenté realizar la instalación y
  configuración local para contar con la trazabilidad automatizada que
  asocia los commits a la IA de manera transparente en la historia de
  Git.

\-\--

**Prompt:**

**\"(.venv) salvaxtraw\\@192 sdlc-electronica-lyla\\\_alice % uv tool
update-shell error: The executable directory
/Users/salvaxtraw/.local/bin is not in PATH\... aider \--model
gemini/gemini-1.5-pro semana5/conversions.py \... Warning:
gemini/gemini-1.5-pro expects these environment variables
GOOGLE\\\_API\\\_KEY: Not set, GEMINI\\\_API\\\_KEY: Not set\"**

**Respuesta de la IA:**

> El problema está en el nombre de la variable de entorno que
> declaraste. En Bash/Zsh, las variables son estrictamente sensibles a
> mayúsculas y minúsculas. Exporta tu llave con el nombre exacto en
> mayúsculas:\
> export GEMINI_API_KEY=\"tu_llave_aqui\"\
> Y vuelve a arrancar Aider con gemini-2.5-pro \[16\].

- Corregí la Configuración de Variables locales: Identifiqué que exporté
  la clave en minúsculas (\`api_key=\"\...\"\`), por lo que Aider no la
  detectaba. Re-exporté la variable en mayúsculas respetando la
  sensibilidad de la terminal macOS.

\-\--

**Prompt:**

**\"Es correcto, ya aparece y ya le dí el prompt que me diste! Me salió
esto: The API provider has rate limited you. Try again later or check
your quotas\... litellm.BadRequestError\... Gemini API has not been used
in project before or it is disabled\...\"**

**Respuesta de la IA:**

> El mensaje SERVICE_DISABLED y PERMISSION_DENIED significa que Aider
> leyó tu llave correctamente, pero el proyecto asociado a tu llave no
> tiene encendido el interruptor maestro de Google AI Studio.\
> Tienes dos opciones:\
> Ruta A: Habilitar la API en la consola de Google.\
> Ruta B (Plan B Oficial): Documentar la falla de infraestructura de
> terceros y avanzar de inmediato con el editor conversacional para no
> congelar el sprint \[18-20\].

- Apliqué Timeboxing y Pivoté al Plan de Contingencia (Plan B): Debido a
  que la API de Google Studio requería habilitar el proyecto y
  posteriormente reportó un \`HTTP 429\` (Rate Limit en la cuota
  gratuita debido a las múltiples peticiones concurrentes de
  verificación de contexto que hace Aider por debajo), decidí aplicar la
  estrategia de contingencia ágil. Generé el archivo manual e integré la
  reflexión de infraestructura de terceros a la bitácora.

\-\--

**Miércoles · Entrada 3 (Code Review y Pruebas Unitarias Destructivas)**

- Origen: Chat \*\"Revisión de Código y Casos Límite\"\*

**Prompt:**

**\"Día 3 · Miércoles --- Code review y tests con IA (3--4 h)\... Revisa
esta clase como un ingeniero senior en un code review. Busca:
violaciones de SOLID, casos borde sin manejar, riesgos de seguridad y
problemas de rendimiento\... \[Pega de
app/services/reading\\\_service.py\]\"**

**Respuesta de la IA:**

> 🕵️‍♂️ 1. Code Review Crítico (ReadingService):\
> - Observación A (Bypass de validación física): En record_reading
> validas los límites físicos, pero en update_reading te saltas las
> reglas de negocio. Un usuario malicioso podría actualizar una lectura
> legítima a 99999.0 °F y romper la base de datos \[24\].\
> - Observación B (Acoplamiento al framework): Importas
> fastapi.HTTPException dentro de la lógica del servicio. Si mañana
> corremos este servicio en un worker (Celery/MQTT) sin web, el sistema
> fallará. Lanza excepciones puras de dominio y que el router las
> traduzca \[24\].

- Acepté y Documenté en AI\\\_CODE\\\_REVIEW\\.md: Acepté ambas
  observaciones técnicas de grado arquitectónico. Inicié el desarrollo
  de la solución bajo la disciplina estricta de TDD.

\-\--

**Prompt:**

**\"Acepto la observación A y B. Si, pasemos a la fase 4\"**

**Respuesta de la IA:**

> \# Fase RED 🔴: Agrega esta prueba en tests/test_services.py para
> demostrar la vulnerabilidad\
> def test_update_reading_bypasses_physical_validation_should_fail():\
> service = ReadingService(FakeReadingRepository(),
> FakeSensorRepository())\
> service.record_reading(sensor_id=1, value=50.0, unit=\"C\")\
> \
> malicious_payload = ReadingUpdate(value=9999.0, unit=\"F\")\
> with pytest.raises(Exception):\
> service.update_reading(reading_id=1, payload=malicious_payload)

- Acepté la Fase RED (TDD): Implementé la prueba destructiva. Corrí la
  suite de Pytest local y verifiqué que fallara legítimamente debido a
  que el sistema asimilaba el dato corrupto en \`update_reading\` sin
  disparar ninguna validación (\`Failed: DID NOT RAISE Exception\`).

\-\--

**Miércoles · Entrada 4 (Manejo de Punto Flotante y Excepciones de
Dominio)**

- Origen: Chat \*\"Revisión de Código y Casos Límite\"\* (Continuación)

**Prompt:**

**\"============================= test session starts
============================== \... FAILED
tests/test\\\_conversions.py::test\\\_celsius\\\_to\\\_fahrenheit\\\_precision\\\_rounding
FAILED
tests/test\\\_services.py::test\\\_update\\\_reading\\\_bypasses\\\_physical\\\_validation\\\_should\\\_fail\"**

**Respuesta de la IA:**

> El test de redondeo falló por la microimprecisión del estándar binario
> IEEE 754 (97.88000000000001 == 97.88).\
> El test de bypass falló exactamente por lo que queríamos (RED) \[28,
> 30\].\
> \
> Para pasar al GREEN:\
> 1. Envuelve el retorno de conversions.py con round(\..., 2).\
> 2. Crea excepciones de dominio en reading_service.py
> (SensorNotFoundError, InvalidUnitError, OutOfRangeError).\
> 3. Agrega \@app.exception_handler en app/main.py para interceptar
> estas excepciones de dominio y retornar los códigos HTTP (404, 400,
> 422) correspondientes \[30\].

- Acepté y Refactoricé a GREEN (Cierre de Deuda Técnica): Saneé las
  imprecisiones de punto flotante en las aserciones de conversión
  térmica.

- Implementé el Desacoplamiento de FastAPI: Extraje del servicio el
  lanzamiento de excepciones de red, sustituyéndolas por excepciones
  puras de dominio (\`SensorNotFoundError\`, \`OutOfRangeError\`).

- Implementé los Exception Handlers en app/main.py: Mapeé globalmente
  las excepciones de negocio a códigos HTTP, blindando la arquitectura y
  dejando la suite completa de Pytest en verde brillante con cobertura
  estelar.

\-\--

**Miércoles · Entrada 5 (Aumentar Cobertura: Inyección de Mocks para
Base de Datos)**

- Origen: Chat \*\"Aumentar Cobertura de Pruebas de Código\"\*

**Prompt:**

**\"Ya no tenemos errores, pero ahora debemos llegar a ese 95% \...
TOTAL Miss 40 Cover 88% FAIL Required test coverage of 95% not
reached.\"**

**Respuesta de la IA:**

> \# tests/test_repositories.py\
> from unittest.mock import MagicMock\
> from sqlalchemy.exc import SQLAlchemyError\
> from app.repositories.reading_repo import SQLAlchemyReadingRepository\
> \
> def test_reading_repo_rollback_on_commit_error():\
> mock_session = MagicMock()\
> mock_session.commit.side_effect = SQLAlchemyError(\"DB Error\")\
> repo = SQLAlchemyReadingRepository(mock_session)\
> \
> with pytest.raises(SQLAlchemyError):\
> repo.add(sensor_id=999, value=10.0, unit=\"C\")\
> mock_session.rollback.assert_called_once()

- Acepté la Inyección de Fallos con Mocks: Para simular escenarios de
  desastres imposibles de forzar físicamente (como caídas o
  interrupciones de red de la base de datos SQL durante la
  confirmación), implementé \`MagicMock\`. Validé determinísticamente
  que ante fallos en \`.commit()\`, el repositorio ejecuta un
  \`.rollback()\` protegiendo la integridad transaccional.

\-\--

**Prompt:**

**\"TOTAL Miss 25 Cover 92% FAIL Required test coverage of 95% not
reached. FAILED
tests/test\\\_services.py::test\\\_sensor\\\_service\\\_update\\\_not\\\_found
FAILED
tests/test\\\_services.py::test\\\_sensor\\\_service\\\_delete\\\_not\\\_found\"**

**Respuesta de la IA:**

> Las pruebas fallaron porque el servicio de sensores aún lanza
> HTTPException(404) y tu aserción en el test esperaba
> SensorNotFoundError \[38\].\
> Corrige tests/test_services.py para que los asserts de
> test_sensor_service\... esperen HTTPException de FastAPI y verifiquen
> el status_code == 404 \[38\].

- Corregí los Criterios de Aserción: Ajusté las pruebas unitarias de la
  capa de servicio para validar el comportamiento real de
  \`sensor_service.py\` (que arroja \`HTTPException\`), resolviendo las
  fallas del pipeline.

- Selle la Cobertura al 96.93%: Agregué pruebas adicionales para cubrir
  los happy paths de eliminación y actualización directa en base de
  datos (\`test_sensor_repo_update_and_delete_success\`), rebasando la
  meta estricta del 95%.

\-\--

**Miércoles · Entrada 6 (Ajuste de Firmas y Mismatch de Alertas)**

- Origen: Chat \*\"Fixing Test Failures and Coverage\"\*

**Prompt:**

**\"FAILED
tests/test\\\_repositories.py::test\\\_reading\\\_repo\\\_rollback\\\_on\\\_commit\\\_error -
AttributeError: \'SQLAlchemyReadingRepository\' object has no attribute
\'create\' \... TOTAL \... 94.74% \[Falta cubrir alert\\\_repo.py y
db\\\_alert\\\_strategy.py\]\"**

**Respuesta de la IA:**

> El error se debe a que la prueba llama a .create() en tu lectura, pero
> tu repositorio utiliza .add() \[46\].\
> Sustituye en tu test repo.create() por repo.add(sensor_id=1,
> value=25.0, unit=\"C\") \[47\].\
> Para el alert_repo.py que tiene baja cobertura, agrega tests mockeando
> la sesión de SQLAlchemy para el método .add() \[48\].

- Corregí el Acoplamiento de Pines en los Mocks: Ajusté el test de
  persistencia para inyectar los valores crudos esperados por la firma
  de \`.add()\` de mi repositorio relacional, mitigando errores de tipo
  de Mypy.

- Implementé el Blindaje en Alertas: Creé la suite
  \`tests/test_alert_repo.py\` aislando el repositorio con
  \`Session(spec=Session)\`. El pipeline de aserciones del validador de
  anomalías subió oficialmente a 96.85% de cobertura total.

\-\--

**Jueves · Entrada 7 (Registro de Decisiones Arquitectónicas - ADR
0001)**

- Origen: Chat \*\"Semana 5: Arquitectura y IA\"\* (Continuación)

**Prompt:**

**\"Día 4 · Jueves --- Documentación asistida y tu primer ADR (3 h) Un
Architecture Decision Record registra una decisión importante y su
porqué. Pide a la IA un borrador desde tus notas y corrígelo con tu
criterio. Crea docs/adr/0001-arquitectura-en-capas.md\"**

**Respuesta de la IA:**

> \# ADR 0001: Arquitectura en capas para SensorHub\
> \
> \## Estado\
> Aceptado\
> \
> \## Contexto\
> En las primeras iteraciones (Semana 0 y 1), la lógica de lectura de
> sensores y las reglas físicas estaban fuertemente acopladas. Al
> evolucionar hacia una API REST con FastAPI (Semana 3), vincular
> directamente los endpoints (routers) con la base de datos (SQLAlchemy)
> generaba un diseño rígido \[51\]\...

- Acepté y Formalicé la Arquitectura del Repositorio: Creé el directorio
  \`docs/adr/\` e implementé el documento
  \`0001-arquitectura-en-capas.md\`. Justifiqué técnicamente por qué se
  adoptó el Monolito Modular de 4 capas.

- Asimilé el Enfoque \"Monolith First\" de Fowler: Integré al README la
  analogía de hardware para las defensas orales, explicando por qué
  iniciar con microservicios introduce costes operativos absurdos antes
  de estabilizar los límites físicos del dominio.

\-\--

**Viernes · Entrada 8 (Detección de Anomalías e Integración OCP)**

- Origen: Chat \*\"Viernes de Cierre y Mejoras Finales\"\*

**Prompt:**

**\"Día 5 · Viernes --- Ejercicio integrador: feature completa asistida
por IA (4--5 h). Feature: detección y notificación de anomalías --- al
recibir una lectura, se evalúa contra un umbral configurable por sensor;
si lo supera, se registra una alerta consultable por API. TDD estricto y
estrategia de alerta intercambiable (OCP, como en la semana 1).\"**

**Respuesta de la IA:**

> \# tests/test_services.py (Fase RED 🔴)\
> def test_record_reading_triggers_anomaly_alert() -\> None:\
> fake_reading = FakeReadingRepository()\
> fake_sensor = FakeSensorRepository()\
> fake_alert = FakeAlertStrategy()\
> \
> service = ReadingService(fake_reading, fake_sensor,
> alert_strategy=fake_alert)\
> service.record_reading(sensor_id=1, value=85.0, unit=\"C\")\
> \
> assert len(fake_alert.alerts_triggered) == 1

- Acepté la Fase RED (TDD de Anomalías): Incorporé la aserción antes de
  modificar el servicio de negocio, validando que el linter arrojase la
  falla de interfaz \`TypeError: got an unexpected keyword argument
  \'alert_strategy\'\`.

\-\--

**Prompt:**

**\"Correcto! \... FAILED
tests/test\\\_services.py::test\\\_record\\\_reading\\\_triggers\\\_anomaly\\\_alert
FAILED
tests/test\\\_services.py::test\\\_record\\\_reading\\\_normal\\\_no\\\_alert\"**

**Respuesta de la IA:**

> \# Fase GREEN 🟢 (app/services/reading_service.py)\
> class ReadingService:\
> def \_\_init\_\_(self, reading_repo: ReadingRepository, sensor_repo:
> SensorRepository, alert_strategy: AlertStrategy \| None = None) -\>
> None:\
> self.\_alert_strategy = alert_strategy\
> \# \...\
> \
> def record_reading(self, sensor_id: int, value: float, unit: str) -\>
> ReadingModel:\
> \# \... logic \...\
> if sensor.anomaly_threshold is not None and value \>
> sensor.anomaly_threshold:\
> if self.\_alert_strategy:\
> self.\_alert_strategy.trigger_alert(sensor_id, value,
> sensor.anomaly_threshold)

- Acepté el Diseño OCP y logré el GREEN: Modifiqué \`ReadingService\`
  inyectando opcionalmente la estrategia de alerta (\`AlertStrategy\`
  Protocol) para no romper los 80 tests unitarios heredados de las
  semanas anteriores. Conecté los cables de persistencia física en base
  de datos mediante el nuevo \`AlertRepository\` y el endpoint \`GET
  /sensors/{id}/alerts\`.

\-\--

**Sábado · Entrada 9 (Cierre de Calidad: README, Trivy y Corrección del
CI)**

- Origen: Chats \*\"Necesito que agreges a este README\...\"\* y
  \*\"Pytest Ignora Carpeta Deprecada\"\*

**Prompt:**

**\"Necesito que agreges a este README lo que hicimos esta semana.
Igualmente, si hay algún nuevo workflow que podamos agregar o un logo
para el repo estaría genial!\"**

**Respuesta de la IA:**

> \# .github/workflows/security.yml\
> name: Security Scan (Trivy)\
> on: \[push, pull_request\]\
> jobs:\
> trivy-scan:\
> runs-on: ubuntu-latest\
> steps:\
> - name: Checkout del código\
> uses: actions/checkout@v4\
> - name: Construir imagen Docker localmente\
> run: docker build -t sensorhub-api:latest .\
> - name: Ejecutar Trivy vulnerability scanner\
> uses: aquasecurity/trivy-action@master\
> with:\
> image-ref: \'sensorhub-api:latest\'

- Acepté la Documentación de Alto Nivel: Reestructuré el \`README.md\`
  incorporando un diagrama de arquitectura interactivo modelado en
  Mermaid y los badges automáticos de calidad del CI/CD de Render.

- Implementé el Workflow de Seguridad (Trivy): Creé el pipeline de
  escaneo de vulnerabilidades automáticas (\`security.yml\`), sumando
  puntos determinantes para alcanzar el grado de Distinción en la
  rúbrica.

\-\--

**Prompt:**

**\"Run alembic upgrade head\... collecting 50 items / 11 errors\...
ModuleNotFoundError: No module named \'deprecated\'\"**

**Respuesta de la IA:**

> \# pyproject.toml\
> \[tool.pytest.ini_options\]\
> testpaths = \[\"tests\"\]

- Corregí la Configuración del Escaneo de Pytest: Las pruebas históricas
  archivadas en \`deprecated/\` generaban fallas de resolución de
  módulos en el contenedor de GitHub Actions. Lo solucioné restringiendo
  la ruta de búsqueda del motor exclusivamente a la carpeta \`tests/\`
  dentro de \`pyproject.toml\`, logrando un paso del build 100% exitoso
  ✅.


---

# Semana4.md

**Semana 4 - Docker, CI/CD y Despliegue**

**Prompts dados: 16**

**Chats creados: 2**

**Lunes · Entrada 1 (Docker desde cero)**

**Prompt:**

**Conteneriza mi aplicación FastAPI con un Dockerfile optimizado
utilizando una imagen base ligera y aprovechando el caché de capas para
las dependencias. Primero, te dejo lo que vamos a ver, lo que debemos
alcanzar para el Viernes, y detalles extra. Asímismo, voy a necesitar
que generes User Stories y Hash para esta semana. Todo esto lo
trabajaremos en una rama \"vacía\" en lugar de solo una rama extra, así
al ver la rama vacía en github, únicamente saldrán los archivos que
estamos trabajando. Día 1 · Lunes --- Docker desde cero (3--4 h)
Recurso: tutorial oficial "Get Started" de Docker
(https\\://docs.docker.com/get-started/, partes 1--5, \\\~60 min hoy):
DOCKERFILE FROM python:3.12-slim WORKDIR /app COPY requirements.txt .
RUN pip install \--no-cache-dir -r requirements.txt COPY . . EXPOSE 8000
CMD \[\"uvicorn\", \"app.main\\:app\", \"\--host\", \"0.0.0.0\",
\"\--port\", \"8000\"\] Construye y corre: docker build -t
sensorhub\\:dev . && docker run -p 8000:8000 sensorhub\\:dev**

**Respuesta:**

> ¡Excelente, ingeniero! Llegamos a la Semana 4, el punto de inflexión
> donde tu software deja de vivir exclusivamente en tu computadora y
> pasa a estar orquestado, automatizado y vivo en internet.\
> \
> Para aislar completamente tu trabajo de esta semana, ejecutaremos el
> flujo con una rama huérfana (orphan branch). En tu terminal de VS Code
> en la raíz de tu proyecto ejecuta:\
> \
> git checkout \--orphan semana4\
> git rm -rf .\
> git status\
> \
> Ahora que tu rama está vacía, copiaremos únicamente el código de
> producción que diseñamos en la Semana 3. No te preocupes por el
> \"funciona en mi máquina\"; el Dockerfile encapsulará todo.\
> \
> Crea tu Dockerfile en la raíz del repositorio con el siguiente
> contenido:\
> \
> FROM python:3.12-slim\
> WORKDIR /app\
> \
> \# dependencias primero: aprovecha la cache de capas\
> COPY requirements.txt .\
> RUN pip install \--no-cache-dir -r requirements.txt\
> \
> COPY . .\
> \
> EXPOSE 8000\
> \
> CMD \[\"uvicorn\", \"app.main:app\", \"\--host\", \"0.0.0.0\",
> \"\--port\", \"8000\"\]\
> \
> Y crea el archivo .dockerignore para evitar inyectar basura en la
> imagen de producción:\
> .venv/\
> \_\_pycache\_\_/\
> \*.db\
> .pytest_cache/\
> tests/\
> \
> Construye y levanta tu contenedor de prueba:\
> docker build -t sensorhub:dev .\
> docker run -p 8000:8000 sensorhub:dev

- Acepté la contenerización con python:3.12-slim: Reduje drásticamente
  el peso del contenedor y eliminé dependencias del sistema operativo
  innecesarias, mitigando posibles vectores de vulnerabilidades.

- Corregí la precedencia de copia de archivos: Aseguré que el comando
  \`COPY requirements.txt .\` se ejecute antes de copiar todo el código
  fuente (\`COPY . .\`). Esto permite que Docker use el caché de capas
  para las dependencias de Python y no reinstale librerías pesadas cada
  vez que modifique una línea de mi código, reduciendo la compilación de
  minutos a segundos.

- Acepté la creación de la rama huérfana (semana4): Permite subir y
  aislar únicamente los archivos correspondientes a esta semana para
  simplificar la revisión por pares del Pull Request sin arrastrar el
  histórico acumulado.

\-\--

**Martes · Entrada 2 (Docker Compose + PostgreSQL)**

**Prompt:**

**Orquesta la API y una base de datos PostgreSQL 16 usando Docker
Compose, y configura Alembic para que la conexión a la base de datos sea
dinámica según el entorno. Día 2 · Martes --- Docker Compose +
PostgreSQL (3--4 h) DOCKER COMPOSE services: api: build: . ports:
\[\"8000:8000\"\] environment: DATABASE\\\_URL:
postgresql+psycopg://sensor\\:secret\\@db:5432/sensorhub depends\\\_on:
\[db\] db: image: postgres:16 environment: POSTGRES\\\_USER: sensor
POSTGRES\\\_PASSWORD: secret POSTGRES\\\_DB: sensorhub volumes:
\[pgdata:/var/lib/postgresql/data\] volumes: pgdata: Modifica db.py para
leer DATABASE\\\_URL del entorno, con SQLite como default local:
os.getenv(\"DATABASE\\\_URL\", \"sqlite:///sensorhub.db\") La URL
postgresql+psycopg:// necesita el driver de PostgreSQL: instala pip
install \"psycopg\[binary\]\" y agrega psycopg\[binary\] a tu
requirements.txt --- sin él verás ModuleNotFoundError al conectar.
Render y otros proveedores pueden entregarte la URL como postgres\\:// o
postgresql:// sin el sufijo del driver. Normalízala en db.py para que
funcione igual en cualquier entorno: import os def
get\\\_database\\\_url() -\> str: url = os.getenv(\"DATABASE\\\_URL\",
\"sqlite:///sensorhub.db\") if url.startswith(\"postgres\\://\"): return
url.replace(\"postgres\\://\", \"postgresql+psycopg://\", 1) if
url.startswith(\"postgresql://\") and \"+psycopg\" not in url: return
url.replace(\"postgresql://\", \"postgresql+psycopg://\", 1) return url
Cierra el día con Alembic (30 min): inicializa las migraciones hoy para
que en la semana 6 sean práctica y no descubrimiento: alembic init
migrations alembic revision \--autogenerate -m \"esquema inicial:
sensors y readings\" alembic upgrade head**

**Respuesta:**

> ¡Excelente guía para el Martes! La orquestación local con Docker
> Compose simulará exactamente un entorno productivo empresarial.\
> \
> Reemplacemos tu archivo app/db.py para que normalice dinámicamente las
> cadenas de conexión:

\# app/db.py

import os

from collections.abc import Generator

from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

def get_database_url() -\> str:

url = os.getenv(\"DATABASE_URL\", \"sqlite:///sensorhub.db\")

if url.startswith(\"postgres://\"):

return url.replace(\"postgres://\", \"postgresql+psycopg://\", 1)

if url.startswith(\"postgresql://\") and \"+psycopg\" not in url:

return url.replace(\"postgresql://\", \"postgresql+psycopg://\", 1)

return url

DATABASE_URL = get_database_url()

\# Si es SQLite, agregamos connect_args para multihilo

connect_args = {\"check_same_thread\": False} if
DATABASE_URL.startswith(\"sqlite\") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):

pass

def get_db() -\> Generator\[Session, None, None\]:

db = SessionLocal()

try:

yield db

finally:

db.close()

> Crea tu archivo docker-compose.yml en la raíz:

version: \'3.8\'

services:

api:

build: .

ports:

\- \"8000:8000\"

environment:

\- DATABASE_URL=postgresql+psycopg://sensor:secret@db:5432/sensorhub

depends_on:

\- db

db:

image: postgres:16-alpine

environment:

\- POSTGRES_USER=sensor

\- POSTGRES_PASSWORD=secret

\- POSTGRES_DB=sensorhub

ports:

\- \"5433:5432\"

volumes:

\- pgdata:/var/lib/postgresql/data

volumes:

pgdata:

> Añade \*\*\`psycopg\[binary\]\`\*\* a tu requirements.txt. Para
> levantar tu infraestructura local y configurar Alembic ejecuta:\
> \
> docker compose up -d \--build alembic init migrations

\* Acepté la normalización de la URL en \`db.py\`: \[4\] Implementé
\`get_database_url()\` para traducir en tiempo de ejecución las URLs
incompatibles (\`postgres://\`) provistas por proveedores PaaS como
Render por la cadena tipada que SQLAlchemy espera
(\`postgresql+psycopg://\`) \[4, 5\].

\* Corregí un conflicto físico de puertos en mi host: \[4\] Como tenía
una instancia local de PostgreSQL corriendo en el puerto \`5432\` de mi
Mac, reconfiguré el mapeo de puertos del servicio de base de datos en
\`docker-compose.yml\` para exponerlo en el host a través del puerto
\`5433:5432\` \[4\]. Esto me permitió conectarme a la base de datos de
Docker sin apagar mi servicio de base de datos local y sin romper la
conectividad interna de los contenedores \[4\].

\* Acepté e instalé \`psycopg\[binary\]\` en \`requirements.txt\`: Evitó
el clásico error \`ModuleNotFoundError\` en mi contenedor de aplicación
\[6\].

\-\--

**Miércoles · Entrada 3 (Pipeline de CI con GitHub Actions)**

**Prompt:**

\*\*Configura un pipeline de Integración Continua (CI) en GitHub Actions
que ejecute Ruff, Mypy y Pytest con una cobertura mínima del 80%.

Día 3 · Miércoles --- Pipeline de CI con GitHub Actions (3--4 h)

.github/workflows/ci.yml

name: CI

on:

push: { branches: \[main\] }

pull_request:

jobs:

test:

runs-on: ubuntu-latest

steps:

\- uses: actions/checkout@v4

\- uses: actions/setup-python@v5

with: { python-version: \"3.12\" }

\- run: pip install -r requirements.txt && pip install pytest pytest-cov
ruff mypy

\- name: Lint

run: ruff check .

\- name: Types

run: mypy app \--ignore-missing-imports

\- name: Tests

run: pytest \--cov=app \--cov-fail-under=80\*\*

**Respuesta:**

> ¡Espectacular, tu pipeline de CI actuará como un guardia de calidad
> impecable en la nube!\
> \
> Crea el archivo en la ruta .github/workflows/ci.yml:\
> \
> name: CI\
> \
> on:\
> push:\
> branches: \[main, semana4-dev\]\
> pull_request:\
> branches: \[main\]\
> \
> jobs:\
> test:\
> runs-on: ubuntu-latest\
> steps:\
> - uses: actions/checkout@v4\
> - uses: actions/setup-python@v5\
> with:\
> python-version: \"3.12\"\
> - name: Install dependencies\
> run: \|\
> pip install -r requirements.txt\
> pip install pytest pytest-cov ruff mypy\
> - name: Lint\
> run: ruff check .\
> - name: Types\
> run: mypy app \--ignore-missing-imports\
> - name: Tests\
> run: pytest \--cov=app \--cov-fail-under=80

- Acepté la validación estricta automatizada de Git: Verifiqué el
  funcionamiento del pipeline en la nube, donde un commit erróneo frena
  automáticamente la integración de código (fase RED) si no pasa las
  aserciones mínimas de calidad.

- Corregí y saneé el linter de manera proactiva: El build falló
  inicialmente debido a errores lógicos y de formateo en mi código de
  producción detectados por Ruff. Lo corregí ejecutando \`ruff check
  \--fix\` localmente antes de realizar el commit verde definitivo
  (GREEN) y habilitar el badge de calidad en el \`README.md\`.

\-\--

**Jueves · Entrada 4 (Infraestructura como Código y Despliegue en
Render)**

**Prompt:**

\\\\Implementa un Health Check endpoint usando TDD y configura la
infraestructura como código en Render.com mediante render.yaml. Día 4 ·
Jueves --- Despliegue continuo en Render (3 h) render.yaml
(infraestructura como codigo) services:

\- type: web name: sensorhub-api runtime: docker plan: free
healthCheckPath: /health envVars:

\- key: DATABASE\\\_URL fromDatabase: { name: sensorhub-db, property:
connectionString } databases:

\- name: sensorhub-db plan: free\\\\

**Respuesta:**

> Excelente. La Infraestructura como Código (IaC) evita configuraciones
> manuales propensas a errores de entorno.\
> \
> Primero, aplicando TDD, escribe tu test en tests/test_api.py:\
> \
> def test_health_endpoint(client):\
> response = client.get(\"/health\")\
> assert response.status_code == 200\
> assert response.json() == {\"status\": \"ok\", \"db\": \"connected\"}\
> \
> Ahora, escribe tu ruta /health en app/main.py para poner la prueba en
> verde:\
> \
> \@app.get(\"/health\")\
> def health(db: Session = Depends(get_db)) -\> dict\[str, str\]:\
> \# Hacemos una consulta rápida de prueba para verificar la BD\
> try:\
> db.execute(text(\"SELECT 1\"))\
> return {\"status\": \"ok\", \"db\": \"connected\"}\
> except Exception:\
> raise HTTPException(status_code=500, detail=\"Database connection
> failed\")\
> \
> Y crea el archivo render.yaml en tu raíz para aprovisionar tu API y
> base de datos relacional de manera automatizada:\
> \
> services:\
> - type: web\
> name: sensorhub-api\
> runtime: docker\
> plan: free\
> healthCheckPath: /health\
> startCommand: alembic upgrade head && uvicorn app.main:app \--host
> 0.0.0.0 \--port 8000\
> envVars:\
> - key: DATABASE_URL\
> fromDatabase: { name: sensorhub-db, property: connectionString }\
> databases:\
> - name: sensorhub-db\
> plan: free

- Acepté la disciplina del flujo TDD: Escribí primero el test que
  fallaba (\`RED\`) en mi local antes de definir la ruta en FastAPI para
  confirmar que el guardián de calidad detectaba la ausencia de la ruta
  y luego la aceptaba en verde (\`GREEN\`).

- Acepté la automatización de la persistencia de producción: Configuré
  en la directiva de arranque de \`render.yaml\` el comando \`alembic
  upgrade head && uvicorn\...\`. Esto garantiza que el motor ejecute
  todas las migraciones físicas de Alembic en producción antes de
  levantar el servidor web, previniendo el error clásico de \"deploy
  exitoso, pero API caída porque no existen las tablas\" en el entorno
  en la nube.

\-\--

**Viernes · Entrada 5 (Alineación de Modelos de Alembic y Resolución de
Conflictos de Git)**

**Prompt:**

**Diagnostica el error \'OperationalError: no such table\' en el
despliegue de Render y soluciona el conflicto de historias para permitir
el Pull Request desde una rama huérfana.**

**Respuesta:**

> ¡El clásico error de base de datos vacía al desplegar en Render!\
> \
> Ocurre porque Alembic no sabe qué modelos existen en tu aplicación.
> SQLAlchemy es perezoso (lazy-loading), y si no importamos
> explícitamente las clases, el generador de Alembic no las escaneará,
> dejando el archivo env.py ciego y generando una migración vacía.\
> \
> Modificaremos migrations/env.py para importar tus modelos:\
> \
> from app.db import Base\
> from app.models.sensor import SensorModel\
> from app.models.reading import ReadingModel\
> \
> target_metadata = Base.metadata\
> \
> Respecto a Git, como semana4 es una rama huérfana sin ancestros
> comunes con main, GitHub rechaza el PR debido al conflicto \"unrelated
> histories\".\
> \
> Ejecuta esto localmente para forzar la sincronización:\
> git checkout semana4\
> git pull origin main \--allow-unrelated-histories\
> \
> Acepta tus cambios correspondientes en VS Code, limpia los marcadores
> del merge conflict y sube:\
> git add .\
> git commit -m \"chore: resolucion de conflicto de fusión con main para
> despliegue\"\
> git push origin semana4

- Corregí la configuración del archivo de migración en la nube: Importé
  manualmente las clases de datos (\`SensorModel\`, \`ReadingModel\`)
  dentro de \`migrations/env.py\` para asegurar que el generador
  autogenerado de Alembic detectara correctamente las tablas e índices
  relacionales en el motor PostgreSQL de Render.

- Corregí el bloqueo de Integración Continua (Git): Dado que la rama
  huérfana \`semana4\` no compartía ningún ancestro común con \`main\`,
  GitHub impedía abrir el Pull Request. Resolví el bloqueo localmente
  forzando el comando \`git merge main \--allow-unrelated-histories\`,
  saneando las diferencias mediante VS Code y empujando una historia
  unificada que desencadenó el Despliegue Continuo (CD) exitoso en
  Render.com.


---

# Semana3.md


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


---

# Semana2.md


### **Prompts dados: 14**

### **Chats creados: 1**

### Lunes · Entrada 1 (Scrum en profundidad)

**Prompt:**
> **Ayúdame a completar mis notas de la Scrum Guide 2020 con los 5 eventos y sus timeboxes, los 3 artefactos con sus compromisos, los 5 valores y la diferencia entre Definition of Done y Criterio de Aceptación, manteniendo estrictamente mi estilo de escritura y terminología en inglés**

**Respuesta:**
````text
```
¡Excelente iniciativa! Mapear Scrum a tu propio estilo técnico asegura que interiorices el framework como una herramienta de entrega y no como simple burocracia.

Aquí tienes la continuación de tus notas para tu archivo Markdown, manteniendo el formato limpio y la terminología estándar en inglés:

# **Eventos con timeboxes**:

#### **El Sprint:**
**Es el corazón de Scrum, un contenedor para todos los demás eventos donde las ideas se transforman en valor.**
* **Timebox:** Un mes o menos para crear consistencia. Un nuevo Sprint comienza inmediatamente después de la conclusión del anterior.
* **Durante el Sprint:** No se realizan cambios que pongan en peligro el Sprint Goal, no disminuye la calidad del producto, y el alcance puede clarificarse y renegociarse con el Product Owner a medida que se aprende más.

#### **Sprint Planning:**
**Inicia el Sprint al establecer el trabajo que se realizará.**
* **Timebox:** Máximo 8 horas para un Sprint de un mes (proporcionalmente menor para Sprints más cortos, ej. 2 horas para un Sprint de una semana).
* **Entregas:** El Sprint Goal (por qué es valioso el Sprint), los elementos del Product Backlog seleccionados (el qué), y el plan de entrega (el cómo, desglosado en tareas).

#### **Daily Scrum:**
**Un evento diario para que los Developers inspeccionen el progreso hacia el Sprint Goal y adapten el Sprint Backlog según sea necesario.**
* **Timebox:** 15 minutos exactos, todos los días a la misma hora y en el mismo lugar.
* **Enfoque:** Diseñar un plan de acción para las próximas 24 horas. No es un estatus jerárquico, es sincronización del equipo.

#### **Sprint Review:**
**Se realiza al final del Sprint para inspeccionar el Increment obtenido y determinar adaptaciones futuras en el Product Backlog.**
* **Timebox:** Máximo 4 horas para un Sprint de un mes.
* **Enfoque:** El Scrum Team y los Stakeholders revisan lo que se logró y discuten el progreso hacia el Product Goal.

#### **Sprint Retrospective:**
**El cierre del Sprint, enfocado en planificar formas de aumentar la calidad y la efectividad del equipo.**
* **Timebox:** Máximo 3 horas para un Sprint de un mes.
* **Enfoque:** Inspeccionar cómo fue el último Sprint con respecto a las personas, las relaciones, los procesos y las herramientas, acordando al menos una mejora concreta para el siguiente ciclo.

---

# **Los 3 Artefactos y sus Compromisos**:

1. **Product Backlog** (Compromiso: **Product Goal**): La lista ordenada y emergente de lo que se necesita para mejorar el producto. El Product Goal describe el estado futuro del producto que sirve como objetivo de planificación.
2. **Sprint Backlog** (Compromiso: **Sprint Goal**): El conjunto de elementos seleccionados más el plan de entrega. El Sprint Goal es el objetivo único del Sprint que da foco a los Developers.
3. **Increment** (Compromiso: **Definition of Done**): El conjunto de todos los elementos del Product Backlog completados durante un Sprint. El Increment es un paso concreto hacia el Product Goal y debe ser utilizable. La Definition of Done es la descripción formal del estado del Increment cuando cumple con las medidas de calidad requeridas.

---

# **Los 5 Valores de Scrum**:
* **Commitment (Compromiso):** Comprometerse a lograr las metas del Scrum Team.
* **Focus (Foco):** Dedicar el esfuerzo a las metas del Sprint para entregar valor.
* **Openness (Apertura):** Transparencia en los desafíos, el trabajo y el estado real del proyecto.
* **Respect (Respeto):** Respetar a los miembros del equipo como personas capaces e independientes.
* **Courage (Coraje):** Coraje para hacer lo correcto y trabajar en problemas difíciles.

---

# **Diferencia crítica: Definition of Done vs. Criterios de Aceptación**:

* **Definition of Done (DoD):** Es el estándar de calidad global y transversal aplicable a todo el software generado en la planta (ej: "cobertura de tests ≥ 80%, ruff check limpio, tipos de mypy sin errores"). Todo Increment debe cumplir la DoD para considerarse terminado.
* **Criterios de Aceptación (Acceptance Criteria):** Son las condiciones específicas de negocio de una única User Story, usualmente escritas en formato Gherkin (Given/When/Then), que definen el comportamiento funcional de esa tarjeta (ej: "si la temperatura es exactamente 35.0 °C, el sistema clasifica la medición como NORMAL").

```

- **Acepté:** La conceptualización de los artefactos y compromisos. Consolidar la Definition of Done como una regla de calidad de infraestructura y el criterio de aceptación como una regla de negocio funcional.
- **Rechacé:** La duda inicial sobre si estructurar el GitHub Project como un repositorio o capa aislada. Tras analizar la diferencia en el SDLC, determiné con criterio propio que el tablero Kanban (Project) debe integrarse de forma nativa en el mismo repositorio para vincular de manera automatizada los Issues con las futuras Pull Requests de Git.

---

**Martes · Entrada 2 (User stories y Gherkin)**
````

### Martes · Entrada 2 (User stories y Gherkin)

**Prompt:**
> **Audita como un ingeniero implacable mi borrador de 7 User Stories con escenarios Gherkin para un sistema de monitoreo IoT de bodega industrial. Señala ambigüedades, casos borde olvidados para TDD y ayúdame a reestructurar el backlog hasta superar las 10 historias con priorización MoSCoW y Story Points en escala Fibonacci**
>
> *(El usuario pegó su borrador inicial de 7 historias en el chat).*

**Respuesta:**
````text
```
¡Tienes un excelente punto de partida! Has demostrado un pensamiento de ingeniería muy sólido al incorporar conceptos como la conversión de unidades (US-05), el filtrado de ruido y el límite de tasa de muestreo (rate limiting de 30 segundos en US-06). Estás pensando en cómo se comporta el hardware en el mundo real y traduciéndolo a software.

Me pongo mi sombrero de auditor técnico implacable. Para que estas historias alcancen el puntaje máximo en tu evaluación y te sirvan como especificaciones exactas para hacer TDD estricto, aquí tienes mi auditoría dividida en observaciones globales y el desglose historia por historia:

### 🔍 3 Hallazgos Arquitectónicos Globales
1. El Rol en la Historia ("Como desarrolladora..."): Estás usando "Como desarrolladora del sistema..." en casi todas tus historias. En el SDLC, la desarrolladora es quien construye el software, no quien lo opera en tiempo de ejecución. Cambia el actor por los usuarios reales (ej. "Como administradora de bodega", "Como operador de planta").
2. Cuidado con las "Cadenas Mágicas" (Magic Strings): En la US-01 mencionas And la id del sensor no es "GHOST_99". "GHOST_99" en el ejemplo de la guía era solo un identificador ficticio. Si lo pones así en tu Gherkin, tu código de producción literalmente tendría que buscar el texto "GHOST_99" para rechazarlo. Cambia esa condición por algo genérico: Given un ID de sensor que no está registrado en el inventario.
3. Modo de lectura vs. escritura en Logs (US-03): En la US-03 dices: And se abre problemlog.md en modo lectura. Si ocurre una excepción o un error de sistema, lo que el software necesita hacer es escribir (modo append), no leerla.

### 📋 Auditoría Historia por Historia (Casos Borde y Ambigüedades)
* US-01 (Verificar conexión): "When obtenga el estado OK". El estado OK es la consecuencia, no la acción. El When debe ser la acción (ej. When el sensor envía su paquete de conexión).
* US-02 (Categorizar sensor nuevo): Pides que el sensor dé "sus primeras 10 lecturas" para ser categorizado. Si leen cada 30 segundos, ¡el sistema tardará 5 minutos en saber el tipo! Es mejor categorizarlo desde el primer payload analizando las unidades (°C, %).
* US-03 (Cuantificar sensores): Error 404 para menos de 10 sensores. El 404 significa Not Found en HTTP. Para la lógica de una bodega industrial, es mucho más preciso lanzar una excepción arquitectónica como InsufficientSensorsException.
* US-04 (Parámetros de lectura): Esta historia se mezcla con las anomalías. Te recomiendo enfocar esta historia netamente en el límite de tasa de muestreo (rate limiting de 30 segundos), validando qué pasa si un sensor intenta enviar datos antes de que pasen los 30 segundos.
* US-05 (Conversor de temperatura): ¿Qué pasa si un sensor en Kelvin envía un valor negativo (ej. -5 K)? El cero absoluto es 0 K; un número negativo físicamente es imposible y debería generar un estado de error (ERR), no convertirse a Celsius.
* US-07 (Alerta por anomalía): La guía pide que el AlertManager maneje una estrategia abstracta que soporte Consola y Archivo. Aquí solo estás probando que manda un mensaje a la consola. Te falta un escenario que verifique que la alerta también se guarda en un archivo de bitácora.
* El Caso Borde más importante para TDD: Dices "lee más de 35°C". ¿Qué debe pasar si el sensor lee exactamente 35.0 °C o exactamente 80.0 %? En tu Gherkin debe quedar estricto si el umbral es inclusivo (>=) o exclusivo (>).

Aquí tienes el Product Backlog reestructurado a 11 historias, calibrado con precisión de ingeniería y estimaciones en la escala Fibonacci (1, 2, 3, 5, 8, 13) y priorización MoSCoW:

#### US-01: Verificar y registrar conexión de sensor nuevo
**Etiqueta:** MoSCoW: Must | **Story Points:** 2
> Como administradora de bodega, quiero que el sistema detecte y registre automáticamente cualquier sensor nuevo que se conecte, para mantener un inventario actualizado de los dispositivos de monitoreo en la planta.
* Scenario: Registro exitoso de sensor nuevo
  * Given un sensor con ID "TEMP_01" que no está registrado en el sistema
  * When el sensor envía su paquete de inicialización y handshake
  * Then el sistema lo registra en el inventario activo con estado "OK"
  * And el dispositivo queda disponible para consulta en el historial de conexiones
* Scenario: Reconexión de sensor ya existente
  * Given un sensor con ID "TEMP_01" que ya existe en el registro del sistema
  * When el sensor envía su paquete de inicialización tras un reinicio
  * Then el sistema restablece su sesión con estado "OK" sin duplicar el registro
  * And se registra el evento de reconexión en el historial

#### US-02: Categorización automática por tipo de medición
**Etiqueta:** MoSCoW: Must | **Story Points:** 3
> Como administradora de bodega, quiero que el sistema clasifique los sensores automáticamente según sus unidades de medición desde su primer payload, para asignarles las reglas de validación y almacenamiento correctas sin tiempos de espera.
* Scenario: Categorización de sensor de temperatura
  * Given un sensor recién conectado que envía un payload de prueba
  * When el payload incluye la unidad de medición en "C", "F" o "K"
  * Then el sistema clasifica el sensor en la categoría "TEMPERATURE"
  * And le asigna el identificador estándar correspondiente (ej. "TEMP_01")
* Scenario: Categorización de sensor de humedad
  * Given un sensor recién conectado que envía un payload de prueba
  * When el payload incluye la unidad de medición en "%H"
  * Then el sistema clasifica el sensor en la categoría "HUMIDITY"
  * And le asigna el identificador estándar correspondiente (ej. "HUM_01")
* Scenario: Rechazo de sensor con unidades desconocidas
  * Given un sensor recién conectado que envía un payload de prueba
  * When el payload incluye unidades no soportadas (ej. "LUMENS" o "PSI")
  * Then el sistema rechaza la conexión con el estado "UNSUPPORTED_TYPE"
  * And elimina el dispositivo del registro temporal

#### US-03: Validación estricta de 10 sensores activos
**Etiqueta:** MoSCoW: Must | **Story Points:** 5
> Como administradora de bodega, quiero que el monitoreo solo inicie cuando haya exactamente 10 sensores calibrados y activos, para garantizar la cobertura térmica y de humedad completa en toda la superficie industrial.
* Scenario: Inicio exitoso con exactamente 10 sensores
  * Given que existen exactamente 10 sensores registrados y activos en el sistema
  * When el sistema inicia el ciclo de monitoreo continuo
  * Then el estado general cambia a "MONITORING_ACTIVE"
  * And el motor de ingesta comienza a procesar lecturas cada 30 segundos
* Scenario: Bloqueo por déficit de sensores (Menos de 10)
  * Given que hay 9 o menos sensores activos en el sistema
  * When se intenta iniciar el ciclo de monitoreo continuo
  * Then el sistema lanza una excepción InsufficientSensorsException
  * And el monitoreo permanece en estado "STOPPED"
  * And se escribe el error de déficit de cobertura en el archivo problemlog.md
* Scenario: Bloqueo por exceso de sensores (Más de 10)
  * Given que hay 11 o más sensores enviando tramas al sistema
  * When se intenta iniciar el ciclo de monitoreo continuo
  * Then el sistema lanza una excepción LimitExceededException
  * And el monitoreo permanece en estado "STOPPED"
  * And se escribe el error de sobrecapacidad en el archivo problemlog.md

#### US-04: Control de tasa de muestreo (Rate Limiting de 30s)
**Etiqueta:** MoSCoW: Must | **Story Points:** 3
> Como administradora de bodega, quiero limitar la recepción de datos de cada sensor a una lectura máximo cada 30 segundos, para evitar la saturación de la base de datos y filtrar ruidos por envíos compulsivos del hardware.
* Scenario: Lectura aceptada respetando el intervalo
  * Given que el sensor "TEMP_01" realizó su última lectura hace 30 segundos o más
  * When envía una nueva lectura válida al sistema
  * Then la lectura se procesa y se almacena en el historial con estado "OK"
* Scenario: Lectura descartada por frecuencia excesiva (Spamming)
  * Given que el sensor "TEMP_01" realizó su última lectura hace 12 segundos
  * When envía una nueva lectura al sistema
  * Then la lectura es descartada por el limitador de frecuencia
  * And se almacena un registro de evento descartado con estado "RATE_LIMIT_EXCEEDED"
  * And no se altera el timestamp de la última lectura válida

#### US-05: Normalización y conversión de temperaturas a Celsius
**Etiqueta:** MoSCoW: Should | **Story Points:** 2
> Como administradora de bodega, quiero que todas las mediciones térmicas en Fahrenheit o Kelvin se conviertan automáticamente a Celsius antes de procesarse, para estandarizar las comparaciones con los umbrales de anomalía del negocio.
* Scenario: Conversión exitosa desde Fahrenheit
  * Given una lectura recibida de "TEMP_02" con un valor de 95.0 y unidad "F"
  * When pasa por el módulo de normalización de datos
  * Then el valor se transforma exactamente a 35.0 con unidad "C"
  * And se almacena en el historial como 35.0 °C
* Scenario: Conversión exitosa desde Kelvin
  * Given una lectura recibida de "TEMP_03" con un valor de 308.15 y unidad "K"
  * When pasa por el módulo de normalización de datos
  * Then el valor se transforma exactamente a 35.0 con unidad "C"
  * And se almacena en el historial como 35.0 °C
* Scenario: Rechazo de valor físicamente imposible en Kelvin (Caso borde TDD)
  * Given una lectura recibida de "TEMP_03" con un valor de -5.0 y unidad "K"
  * When pasa por el módulo de normalización de datos
  * Then el sistema rechaza la medición lanzando un InvalidPhysicalValueException
  * And la lectura se registra con estado "ERR_OUT_OF_BOUNDS"

#### US-06: Validación de integridad del payload de lectura
**Etiqueta:** MoSCoW: Must | **Story Points:** 3
> Como administradora de bodega, quiero verificar que los paquetes de datos recibidos contengan formatos numéricos válidos y estén dentro del rango físico del sensor, para prevenir caídas del sistema por datos corruptos o cortocircuitos.
* Scenario: Payload íntegro y dentro de rango
  * Given el sensor "HUM_01" envía una lectura de 45.5% con timestamp UTC válido
  * When el sistema valida la estructura del mensaje
  * Then la lectura se marca con estado "OK" y se pasa al detector de anomalías
* Scenario: Payload con datos corruptos (No numérico)
  * Given un sensor envía una trama donde el valor de lectura es la cadena "ERROR_READ"
  * When el sistema intenta parsear el valor flotante
  * Then se captura un error de conversión y la lectura se marca como "ERR_CORRUPT_PAYLOAD"
  * And el evento se registra en la bitácora de problemas
* Scenario: Lectura fuera de rango físico del sensor (Hardware Fault)
  * Given el sensor "TEMP_01" envía una lectura de 450.0 °C
  * When el sistema compara el valor con los límites de operación del hardware (-50 a 100 °C)
  * Then la lectura se descarta por fallo de sensor y se marca como "ERR_HARDWARE_FAULT"

#### US-07: Detección de anomalías térmicas y de humedad con alerta en consola
**Etiqueta:** MoSCoW: Must | **Story Points:** 5
> Como administradora de bodega, quiero que el sistema evalúe cada lectura normalizada contra los umbrales de seguridad y emita una alerta visual en consola al superarlos, para que los operadores reaccionen de inmediato ante riesgos en la mercancía.
* Scenario: Umbral de temperatura superado (Anomalía detectada)
  * Given un sensor "TEMP_01" que registra una lectura normalizada de 35.1 °C
  * And un detector configurado con el umbral límite inyectado de 35.0 °C
  * When la lectura es evaluada por el AnomalyDetector
  * Then se genera un evento de anomalía con severidad "WARNING"
  * And el AlertManager imprime el mensaje "ALERTA: TEMP_THRESHOLD_BREACHED en TEMP_01 [35.1 °C]" en la consola
* Scenario: Umbral de humedad superado (Anomalía detectada)
  * Given un sensor "HUM_01" que registra una lectura de 80.5 %
  * And un detector configurado con el umbral límite inyectado de 80.0 %
  * When la lectura es evaluada por el AnomalyDetector
  * Then se genera un evento de anomalía con severidad "WARNING"
  * And el AlertManager imprime el mensaje "ALERTA: HUM_THRESHOLD_BREACHED en HUM_01 [80.5 %]" en la consola
* Scenario: Valor en el límite exacto no genera alerta (Caso borde TDD estricto)
  * Given un sensor "TEMP_01" que registra una lectura normalizada de exactamente 35.0 °C
  * When la lectura es evaluada por el AnomalyDetector
  * Then no se genera ninguna anomalía
  * And el sistema clasifica la medición con estado "NORMAL"

#### US-08: Estrategia de persistencia de alertas en archivo de bitácora
**Etiqueta:** MoSCoW: Must | **Story Points:** 3
> Como administradora de bodega, quiero que todas las alertas de anomalías también se escriban en un archivo persistente del sistema, para mantener un historial de incidentes auditable a largo plazo sin depender de la consola.
* Scenario: Escritura de alerta en archivo log
  * Given el AlertManager tiene configurada la estrategia de salida FileAlertStrategy apuntando a alerts.log
  * When se activa una alerta de tipo "TEMP_THRESHOLD_BREACHED" para el sensor "TEMP_01"
  * Then el sistema añade una nueva línea al archivo alerts.log con el timestamp exacto, ID del sensor y valor medido
  * And el archivo conserva las alertas anteriores sin sobrescribirlas (modo append)
* Scenario: Fallo de escritura en disco sin detener la aplicación
  * Given que el archivo alerts.log está bloqueado o sin permisos de escritura
  * When el AlertManager intenta escribir una nueva alerta en el disco
  * Then se captura una excepción de E/S (IOException)
  * And el sistema redirige la alerta a la salida de emergencia en consola sin interrumpir el monitoreo

#### US-09: Simulación de lecturas con distribución gaussiana (Extensión Alto Potencial)
**Etiqueta:** MoSCoW: Could | **Story Points:** 8
> Como administradora de bodega, quiero disponer de un simulador de sensores que genere datos sintéticos usando una distribución normal (gaussiana), para probar el rendimiento del sistema de monitoreo y las alertas bajo condiciones de operación realistas sin hardware conectado.
* Scenario: Generación de lecturas en rango normal
  * Given un SensorSimulator configurado con media de 22.0 °C y desviación estándar de 2.0 °C
  * When se ejecutan 60 ciclos de simulación
  * Then el 95% de las lecturas generadas se mantienen dentro del rango de 18.0 °C a 26.0 °C
  * And las lecturas son inyectadas exitosamente al sistema como si vinieran de sensores físicos
* Scenario: Inyección de anomalía sintética
  * Given el simulador operando en ciclo continuo
  * When se activa el trigger de estrés de prueba inject_anomaly=True
  * Then el simulador fuerza la generación de un valor gaussiano atípico superior a 35.0 °C
  * And el sistema reacciona activando toda la cadena de alertas en menos de 100 ms

#### US-10: Consulta auditable de historial por rango de tiempo
**Etiqueta:** MoSCoW: Should | **Story Points:** 3
> Como administradora de bodega, quiero filtrar y descargar el historial de mediciones de un sensor especificando una fecha y hora de inicio y fin, para analizar tendencias o demostrar el cumplimiento ambiental ante auditores de calidad.
* Scenario: Búsqueda de lecturas en rango válido
  * Given un sensor "TEMP_01" con 1000 lecturas almacenadas en la base de datos
  * When consulto el historial para el intervalo entre "2026-07-21 08:00:00" y "2026-07-21 12:00:00"
  * Then el sistema retorna un listado cronológico con únicamente las lecturas registradas en esa ventana
  * And el listado incluye el valor, la unidad y el estado de cada medición
* Scenario: Consulta en rango sin lecturas
  * Given una consulta al historial para una ventana de tiempo futura o sin actividad
  * When se ejecuta la búsqueda
  * Then el sistema retorna una lista vacía []
  * And responde con un mensaje informativo de "No hay registros en el periodo seleccionado"

#### US-11: Alerta combinada de alta criticidad (Degradación térmica y humedad)
**Etiqueta:** MoSCoW: Could | **Story Points:** 5
> Como administradora de bodega, quiero que el sistema active una alarma de criticidad máxima si un sector de la bodega supera el umbral de temperatura y el de humedad simultáneamente, para identificar condiciones extremas que estropearán el inventario de forma inminente.
* Scenario: Activación de alerta crítica combinada
  * Given un sensor de temperatura "TEMP_01" registrando 36.5 °C
  * And un sensor de humedad "HUM_01" en el mismo sector registrando 85.0 % dentro de la misma ventana de 30 segundos
  * When ambas lecturas son procesadas por el motor de reglas
  * Then el sistema emite una alarma de grado "CRITICAL_ENVIRONMENTAL_HAZARD"
  * And activa simultáneamente las alertas en consola y en el archivo de bitácora con prioridad alta

```

- **Acepté:** La corrección en el rol del actor a "administradora de bodega", de manera que el valor se oriente a la operación y reglas de negocio reales.
- **Acepté:** Reemplazar las cadenas estáticas de pruebas como **`"GHOST_99"`** por validaciones lógicas dinámicas del inventario en las pruebas unitarias y fakes.
- **Rechacé y Corregí:** El diseño del log de errores en la US-03, que abría el archivo **`problemlog.md`** en "modo lectura". Corregí el requerimiento del sistema para persistir la excepción en modo append (escritura de agregación) para no interrumpir el flujo del microcontrolador.
- **Acepté:** Ajustar los operadores de frontera para el detector (operador mayor estricto **`>`**), lo cual nos brindó un criterio matemático determinista (el valor exacto de 35.0 °C es NORMAL) para codificar bajo TDD estricto.

---

**Miércoles · Entrada 3 (TDD estricto)**
````

### Miércoles · Entrada 3 (TDD estricto)

**Prompt:**
> **Guíame paso a paso para implementar SensorRegistry, AnomalyDetector y AlertManager siguiendo un ciclo TDD estricto (Red-Green-Refactor), aplicando inyección de dependencias para umbrales y el patrón Strategy para las alertas**

**Respuesta:**
`````text
````
¡Espectacular! Ver ese git log en la terminal alternando entre RED, GREEN y REFACTOR es la prueba de que estás dominando la disciplina de TDD.

Para cumplir con la meta de tener la lógica de negocio blindada, aplicaremos los 5 ciclos de desarrollo guiado por pruebas paso a paso:

---

### CICLO 1: Manejo de sensor desconocido (US-01)

#### 1. RED 🔴 (test_registry.py)
Creemos primero el test que falla porque el código no existe. Escribe únicamente esta función en `semana2/eval1/test_registry.py`:

```python
import pytest
from semana2.eval1.registry import SensorRegistry, SensorNotFoundError

def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST_99")

````

Al ejecutar **`python -m pytest`** desde la raíz, debe fallar con ImportError porque **`registry.py`** no existe.

- Commit: **`test(registry): especificar SensorNotFoundError para id desconocido (RED) - US-01`**

**2. GREEN 🟢 (registry.py)**

Crea **`semana2/eval1/registry.py`** y escribe el código mínimo absoluto para pasar la aserción:

```
class SensorNotFoundError(Exception):
    pass

class SensorRegistry:
    def get(self, sensor_id: str) -> None:
        raise SensorNotFoundError()

```

Al correr pytest, el test pasa a verde (1 passed).

- Commit: **`feat(registry): implementar busqueda y excepcion de sensor desconocido (GREEN) - US-01`**

**3. REFACTOR 🔵 (registry.py)**

No hay mucho que limpiar en esta etapa, pero confirmamos con Ruff y Mypy que el tipado y el estilo son correctos.

- Commit: **`refactor(registry): aplicar tipado estricto inicial en SensorRegistry (REFACTOR)`**

---

**CICLO 2: Registro exitoso y duplicados (US-01)**

**1. RED 🔴 (test\_registry.py)**

Añade las pruebas para el registro exitoso y duplicados en **`semana2/eval1/test_registry.py`**:

```
def test_register_sensor_successfully():
    registry = SensorRegistry()
    registry.register("TEMP_01")
    assert registry.count() == 1

def test_register_existing_sensor_does_not_duplicate():
    registry = SensorRegistry()
    registry.register("TEMP_01")
    registry.register("TEMP_01")
    assert registry.count() == 1

```

pytest fallará porque los métodos **`register`** y **`count`** no existen.

- Commit: **`test(registry): verificar registro exitoso y reconexion sin duplicados (RED) - US-01`**

**2. GREEN 🟢 (registry.py)**

Implementa la lógica funcional en **`semana2/eval1/registry.py`**:

```
class SensorRegistry:
    def __init__(self) -> None:
        self._sensors: set[str] = set()

    def get(self, sensor_id: str) -> str:
        if sensor_id not in self._sensors:
            raise SensorNotFoundError()
        return sensor_id

    def register(self, sensor_id: str) -> None:
        self._sensors.add(sensor_id)

    def count(self) -> int:
        return len(self._sensors)

```

Toda la suite de pruebas (3 tests) pasa en verde.

- Commit: **`feat(registry): agregar metodos register y count con control de duplicados (GREEN) - US-01`**

**3. REFACTOR 🔵 (registry.py)**

Añadiremos docstrings profesionales a nuestra clase y métodos:

```
class SensorRegistry:
    """Inventario en memoria para registrar sensores y evitar duplicados de hardware."""
    # ... metodos con docstrings ...

```

- Commit: **`refactor(registry): agregar docstrings formales al inventario de sensores (REFACTOR)`**

---

**CICLO 3: Detección de anomalías con inyección de dependencias (US-07)**

**1. RED 🔴 (test\_detector.py)**

Escribe el test para el detector inyectándole los umbrales en **`semana2/eval1/test_detector.py`**:

```
import pytest
from semana2.eval1.models import SensorReading
from semana2.eval1.detector import AnomalyDetector

def test_temperature_anomaly_detected_above_threshold():
    # Inyectamos el umbral (35.0 C) en lugar de hardcodearlo
    detector = AnomalyDetector(temp_threshold=35.0, hum_threshold=80.0)
    reading = SensorReading(sensor_id="TEMP_01", category="TEMPERATURE", value=36.5, unit="C")
    assert detector.is_anomalous(reading) is True

```

Falla con ImportError porque no existen los archivos de producción.

- Commit: **`test(detector): verificar que temperatura sobre umbral genere anomalia (RED) - US-07`**

**2. GREEN 🟢 (models.py y detector.py)**

Crea **`semana2/eval1/models.py`** para modelar la lectura inmutable:

```
from dataclasses import dataclass

@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    category: str
    value: float
    unit: str

```

Y crea **`semana2/eval1/detector.py`** para procesar el umbral inyectado:

```
from semana2.eval1.models import SensorReading

class AnomalyDetector:
    def __init__(self, temp_threshold: float, hum_threshold: float) -> None:
        self.temp_threshold = temp_threshold
        self.hum_threshold = hum_threshold

    def is_anomalous(self, reading: SensorReading) -> bool:
        if reading.category == "TEMPERATURE":
            return reading.value > self.temp_threshold
        return False

```

La suite pasa en verde.

- Commit: **`feat(detector): implementar modelo SensorReading y detector con umbrales inyectados (GREEN) - US-07`**

**3. REFACTOR 🔵 (test\_detector.py)**

El linter Ruff nos avisa que el archivo **`test_detector.py`** tiene una importación huérfana de **`import pytest`** que no estamos usando. Lo eliminamos para limpiar las dependencias.

- Commit: **`refactor(detector): eliminar importaciones sin uso en tests y validar estilo (REFACTOR)`**

---

**CICLO 4: Humedad y Frontera Matemática (US-07)**

**1. RED 🔴 (test\_detector.py)**

Añade las pruebas para humedad y el límite exacto en **`semana2/eval1/test_detector.py`**:

```
def test_humidity_anomaly_detected_above_threshold():
    detector = AnomalyDetector(temp_threshold=35.0, hum_threshold=80.0)
    reading = SensorReading(sensor_id="HUM_01", category="HUMIDITY", value=82.4, unit="%")
    assert detector.is_anomalous(reading) is True

def test_exact_boundary_value_is_not_an_anomaly():
    detector = AnomalyDetector(temp_threshold=35.0, hum_threshold=80.0)
    reading = SensorReading(sensor_id="TEMP_01", category="TEMPERATURE", value=35.0, unit="C")
    assert detector.is_anomalous(reading) is False

```

La de humedad falla porque nuestro código de producción retorna False por defecto para categorías que no son TEMPERATURE.

- Commit: **`test(detector): verificar umbral de humedad y caso borde en el limite exacto (RED) - US-07`**

**2. GREEN 🟢 (detector.py)**

Actualiza **`semana2/eval1/detector.py`** con una estructura DRY limpia:

```
class AnomalyDetector:
    def __init__(self, temp_threshold: float, hum_threshold: float) -> None:
        self.temp_threshold = temp_threshold
        self.hum_threshold = hum_threshold

    def is_anomalous(self, reading: SensorReading) -> bool:
        thresholds = {
            "TEMPERATURE": self.temp_threshold,
            "HUMIDITY": self.hum_threshold
        }
        limit = thresholds.get(reading.category)
        if limit is None:
            return False
        return reading.value > limit

```

Los 6 tests acumulados pasan en verde.

- Commit: **`feat(detector): agregar soporte para humedad y validar comportamiento en frontera (GREEN) - US-07`**

**3. REFACTOR 🔵 (detector.py)**

Revisamos que la inyección de dependencias cumpla con Mypy strict y el linter Ruff.

- Commit: **`refactor(detector): aplicar principio DRY unificando evaluacion de umbrales (REFACTOR)`**

---

**CICLO 5: AlertManager con patrón Strategy (US-08)**

**1. RED 🔴 (test\_alerts.py)**

Creemos **`semana2/eval1/test_alerts.py`** usando las fixtures **`capsys`** y **`tmp_path`** de pytest para aislar el I/O físico:

```
import os
from semana2.eval1.alerts import AlertManager, ConsoleAlertStrategy, FileAlertStrategy

def test_console_alert_strategy_prints_message(capsys):
    strategy = ConsoleAlertStrategy()
    manager = AlertManager(strategy)
    manager.alert("TEMP_01", "TEMP_THRESHOLD_BREACHED", 36.5)
    captured = capsys.readouterr()
    assert "ALERTA: TEMP_THRESHOLD_BREACHED en TEMP_01 [36.5]" in captured.out

def test_file_alert_strategy_appends_to_file(tmp_path):
    log_file = tmp_path / "alerts.log"
    strategy = FileAlertStrategy(str(log_file))
    manager = AlertManager(strategy)
    manager.alert("TEMP_01", "TEMP_THRESHOLD_BREACHED", 36.5)
    
    assert log_file.exists()
    with open(log_file, "r") as f:
        content = f.read()
    assert "TEMP_01" in content
    assert "TEMP_THRESHOLD_BREACHED" in content

```

Falla con ImportError porque el módulo **`alerts.py`** no existe.

- Commit: **`test(alerts): verificar envio de alertas a consola y archivo (RED) - US-08`**

**2. GREEN 🟢 (alerts.py)**

Crea **`semana2/eval1/alerts.py`** con el protocolo intercambiable (Strategy) y las estrategias concretas:

```
from typing import Protocol

class AlertStrategy(Protocol):
    def send(self, sensor_id: str, alert_type: str, value: float) -> None:
        ...

class ConsoleAlertStrategy:
    def send(self, sensor_id: str, alert_type: str, value: float) -> None:
        print(f"ALERTA: {alert_type} en {sensor_id} [{value}]")

class FileAlertStrategy:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def send(self, sensor_id: str, alert_type: str, value: float) -> None:
        with open(self.filepath, "a") as f:
            f.write(f"{sensor_id},{alert_type},{value}\n")

class AlertManager:
    def __init__(self, strategy: AlertStrategy) -> None:
        self._strategy = strategy

    def alert(self, sensor_id: str, alert_type: str, value: float) -> None:
        self._strategy.send(sensor_id, alert_type, value)

```

La suite completa (8 tests) pasa en verde.

- Commit: **`feat(alerts): implementar patron Strategy con soporte consola y archivo (GREEN) - US-08`**

**3. REFACTOR 🔵 (alerts.py)**

Saneamos los imports y agregamos tipado estricto a las interfaces.

- Commit: **`refactor(alerts): asegurar tipado de firma y formato de salida en alertas (REFACTOR)`**

```
* **Acepté:** El diseño arquitectónico completo con inyección de dependencias en `AnomalyDetector` [20, 23] y el patrón Strategy mediante `Protocol` en `AlertManager` [20, 24]. Esto nos permitió alcanzar un **99% de cobertura total** de la suite de pruebas [25].
* **Rechacé y Corregí:** El primer error de entorno al correr pytest (`ModuleNotFoundError: No module named 'semana2'`) [26]. Identifiqué que el PYTHONPATH local de macOS no estaba mapeando la carpeta raíz [27]. Lo corregí usando el comando estandarizado `python -m pytest` y añadiendo los archivos de inicialización `__init__.py` necesarios en cada nivel para habilitar la importación jerárquica [27-30].
* **Corregí:** Un fallo de análisis estático en el Refactor del ciclo 3, donde la IA sugirió un `import pytest` redundante en `test_detector.py` [20, 31]. Al correr `ruff check .` detectamos la importación inútil y la eliminamos para mantener un código limpio antes de sellar el commit [20, 31].
`````

---

#### Jueves · Entrada 4 (DoD y Calidad Automatizada)

**Prompt:**
> > **Ayúdame a redactar la Definition of Done estricta, configurar pyproject.toml para automatizar la calidad (cobertura >= 80%, ruff, mypy) y generar los artefactos Scrum finales (Sprint Planning y Retrospective) basados en nuestro historial** [32, 33]

**Respuesta:**
`````text
```text
¡Excelente progreso técnico! Con una cobertura del 99% y el historial de Git impecable, tu lunes-miércoles fue espectacular.

Para hoy, Jueves (Definition of Done y Calidad Automatizada), abordaremos tres entregables:
1. El contrato escrito de calidad (DEFINITION_OF_DONE.md).
2. La automatización de la calidad centralizada en pyproject.toml para que pytest, ruff y mypy fuercen las reglas.
3. El cierre ágil: Sprint Planning del Sprint 1 y Retrospective del Sprint 0.

Aquí tienes los archivos completos:

### 1. semana2/DEFINITION_OF_DONE.md:
---
# Definition of Done (DoD) - SensorHub

Este documento define el estándar de calidad innegociable para cualquier incremento de software en el proyecto SensorHub. Ningún Issue, User Story o Tech Chore se moverá a "Done" en el tablero Kanban si no cumple con el 100% de estos criterios:

#### 1. Calidad y Verificación Estática
* **Linting:** El comando `python -m ruff check .` debe ejecutarse sin advertencias ni errores de formato.
* **Tipado:** El comando `python -m mypy .` en modo estricto (`strict = true`) debe completarse con éxito, sin tipos dinámicos implícitos (`Any`) ni firmas sin anotar.

#### 2. Robustez y Testing (TDD)
* **Precedencia de Pruebas:** Cada cambio en la capa de lógica debe estar precedido por su test en rojo en el historial de Git, demostrando la disciplina del TDD.
* **Cobertura:** La suite de pruebas debe mantener una cobertura total del código en la carpeta `app/` (o la carpeta de evaluación) de **≥ 80%** (frenado por `--cov-fail-under`).
* **Casos Límite:** Los tests deben incluir al menos un caso de frontera matemática (boundary values) y un escenario de datos inválidos/excepciones de dominio.

#### 3. Integración de Ramas
* **Aislamiento:** Todo el trabajo debe desarrollarse en ramas de características (`feature/...`) y unirse a `main` únicamente mediante un Pull Request.
* **Trazabilidad:** Cada commit debe usar prefijos estandarizados (`feat:`, `test:`, `refactor:`, `docs:`, `chore:`) vinculando el número de Issue correspondiente.
---

### 2. pyproject.toml (Reglas de Calidad Automatizadas en la raíz):
```toml
[tool.pytest.ini_options]
addopts = "--cov=semana2/eval1 --cov-report=term-missing --cov-fail-under=80"

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
# E: Errores de estilo, F: Errores lógicos, I: Orden de imports, UP: Sintaxis moderna, B: Bugs comunes (flake8-bugbear)
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.12"
strict = true
disallow_untyped_defs = true
ignore_missing_imports = true

````

**3. semana2/SPRINT\_PLANNING.md:**

---

**Sprint 1 Planning - SensorHub**

**Sprint Goal:** Implementar y blindar el núcleo de negocio para ingesta y validación de sensores, garantizando que el sistema sea estable y cumpla con el rate limiting antes del empaquetado web.

- **Duración:** 1 Semana.
- **Capacidad del Equipo:** 1 Developer (40 horas).
- **Historias Seleccionadas del Backlog:**
  1. **US-01:** CRUD de Sensores (Must - 2 SP): Registrar y evitar duplicados.
  2. **US-04:** Control de tasa de muestreo (Must - 3 SP): Limitador de 30 segundos.
  3. **US-05:** Conversor de temperatura (Should - 2 SP): Conversión Celsius y cero absoluto.
  4. **US-06:** Validación del payload (Must - 3 SP): Integración e inmunidad ante basura.
- **Tareas desglosadas (Todas ≤ 4 horas):**
  - [ ] [US-01-T01] Crear modelo de datos inmutable para sensores (2h).
  - [ ] [US-01-T02] Implementar validación de handshake inicial en SensorRegistry (3h).
  - [ ] [US-04-T01] Escribir lógica de timestamps para evaluar diferencia de 30s (2h).
  - [ ] [US-04-T02] Crear cola de persistencia temporal para última lectura válida (3h).
  - [ ] [US-05-T01] Crear funciones puras matemáticas de conversión (F y K a C) (1.5h).
  - [ ] [US-05-T02] Integrar excepción de cero absoluto en conversor (2h).

---

**4. semana2/RETROSPECTIVE.md:**

---

**Sprint 0 Retrospective - SensorHub**

**1. ¿Qué salió bien?**

- El ciclo TDD Red-Green-Refactor se ejecutó con absoluta disciplina, logrando un historial de commits limpio y alternado.
- Se alcanzó una cobertura estelar del 99% en las clases núcleo.
- El pyproject.toml centraliza y automatiza todas las reglas de calidad de la DoD.

**2. ¿Qué podemos mejorar?**

- Al principio se perdieron horas lidiando con errores de PYTHONPATH de Python en macOS (**`ModuleNotFoundError`**).
- Algunas sugerencias de la IA incluían importaciones huérfanas que rompían el linter.

**3. Acción concreta de mejora (Sprint 1):**

- **Implementar un checklist de scaffolding:** Cada vez que creemos un paquete o iniciemos un día, se creará el respectivo **`__init__.py`** y usaremos únicamente **`python -m pytest`** desde la raíz como estándar innegociable.

---

````
* **Acepté:** El contrato de calidad de la `Definition of Done` [5, 32, 34], la configuración en `pyproject.toml` para frenar automáticamente la ejecución del build si baja del 80% de cobertura [5, 34], y los artefactos de la planeación y retrospectiva [5, 35].
* **Rechacé y Corregí (Bloqueo de Git por caracteres especiales):** Al intentar crear mi rama local con `git checkout -b feature/sprint_&_restrospective`, la terminal de macOS interpretó el símbolo `&` como un operador de subproceso en segundo plano, rompiendo la línea y levantando una rama huérfana incompleta (`feature/sprint_`) [36-38].
* **Solución de Git y Divergencia de Historias:**
  1. Completé y guardé los commits en la rama local para asegurar los archivos `SPRINT_PLANNING.md` y `RETROSPECTIVE.md` [37, 38].
  2. Al intentar hacer `git push` a `main`, Git rechazó la acción (`fetch first / non-fast-forward`) debido a que se habían hecho modificaciones directas desde la interfaz web de GitHub (la creación del Project y sus issues) que no existían localmente [37].
  3. Ejecuté `git config pull.rebase false` para establecer la estrategia de merge tradicional [37].
  4. Realicé `git pull origin main --allow-unrelated-histories` para unificar ambos árboles genealógicos [37, 39].
  5. Esto provocó un **Merge Conflict** en `AI_LOG.md` [40]. Abrí VS Code, seleccioné la opción **Accept Both Changes** para conservar las reflexiones locales junto con los issues mapeados de la web, limpié los marcadores (`<<<<<<<`, `=======`, `>>>>>>>`) [41], y ejecuté:
     ```bash
     git add AI_LOG.md
     git commit -m "chore: resolucion de conflictos de fusion en bitacora"
     git push origin main
     ```
     La terminal y el pipeline en GitHub Actions quedaron limpios y en verde brillante [42].

---

#### Viernes · Entrada 5 (Mejoras y Consolidación)

*Este día no cuenta con entrada ya que se trabajó los 4 días anteriores en el proyecto, por ende no se realizó ninguna modificación este día [5, 43].*

---

````
`````


---

# Semana1.md


### Prompts dados: 23

### Chats creados: 1

---

## Prompt (Lunes)

> Mapea una lectura de sensor de C a Python moderno usando dataclasses inmutables, enums, tipado estructural (`Protocol`) y 5 funciones puras de procesamiento.

### Respuesta

> ¡Excelente trabajo completando el Checkpoint de la Semana 0!
>
> Establecemos el **Pacto de Trabajo**: la IA propone estructuras y código limpio, pero tú debes auditar y entender cada línea. Si algo no lo puedes defender, lo borramos y lo reescribimos.
>
> Para hoy, Lunes (Python Idiomático para ingenieros de C), abordaremos:
>
> 1. **Modelado de Dominio (De `struct` y `#define` a Enum y Dataclass):** En Python moderno, representamos una lectura (`Reading`) usando `@dataclass(frozen=True)`. Al hacerla inmutable, evitamos efectos secundarios de punteros de C en memoria.
> 2. **Abstracción con Protocol (Tipado Estructural):** Definiremos un contrato de interfaz `Sensor` usando `typing.Protocol`.
> 3. **5 Funciones Puras:** Funciones deterministas en `sensor_utils.py` que procesen datos generando copias (`replace`) sin modificar la entrada.

### Resultado / Aprendizaje

* **Acepté el modelado de datos inmutable:** Adopté **`@dataclass(frozen=True)`** para definir la estructura **`Reading`** y asegurar que los datos no puedan ser mutados accidentalmente, mitigando efectos colaterales de punteros.
* **Rechacé y corregí la ruta de ejecución de Mypy:** La IA sugirió correr Mypy posicionada dentro de la subcarpeta **`semana1/`**, lo cual rompía la resolución de imports de módulos absolutos. Corregí la metodología de calidad, obligándome a ejecutar todos los linters siempre desde el directorio raíz del proyecto.

---

## Prompt (Martes)

> Reimplementa una máquina de estados finita (FSM) orientada a objetos para experimentar el estilo OO frente al C procedural, con 4 tests unitarios.

### Respuesta

> El corazón del firmware robusto embebido es la **Máquina de Estados Finitos (FSM)**. En C, típicamente se implementa con variables globales y un `switch-case` gigante en el superloop, lo cual genera alto acoplamiento y transiciones ilegales invisibles.
>
> En Python y Orientación a Objetos, encapsulamos el estado y sus transiciones válidas dentro de una clase, controlando los errores mediante excepciones personalizadas.
>
> Crearemos una FSM para un **Semáforo de la Bodega (`TrafficLightFSM`)** usando un mapeo **O(1)** de transiciones válidas en un diccionario.

### Resultado / Aprendizaje

* **Rechacé el primer diseño genérico de FSM:** La IA propuso un diseño de FSM para un nodo IoT complejo con múltiples excepciones personalizadas, el cual se desviaba de la especificación técnica estricta de la guía.
* **Acepté la refactorización a semáforo (`TrafficLightFSM`):** Implementé la máquina de estados basándome en un mapeo limpio **`O(1)`** usando **`TrafficLightState`** (`Enum`), encapsulando de forma segura el contador de ciclos sin variables globales.
* **Acepté los 4 tests unitarios de pytest:** Validé de forma estricta los escenarios del ciclo de vida del semáforo: estado inicial, transición `RED -> GREEN`, ciclo completo de retorno a `RED`, y conteo exacto de ciclos acumulados.

---

## Prompt (Miércoles)

> Implementa los tres primeros principios SOLID (S, O y L) con el código base y las firmas exactas indicadas en la guía para `SensorReader`, `AlertStrategy`, `AnomalyDetector` y `process_sensor`.

### Respuesta

> Excelente. Enfrentamos los tres primeros principios de **SOLID** aplicados al dominio de IoT industrial:
>
> * **SRP:** Desacoplamos la lectura física del sensor (`SensorReader`) de la persistencia en disco (`DataLogger`).
> * **OCP:** Diseñamos clases de alertas que hereden de una clase abstracta `AlertStrategy` (`ABC`). Añadir `EmailAlert` no modificará las clases de negocio existentes.
> * **LSP:** Las subclases de sensores deben ser completamente intercambiables sin alterar la lógica de procesamiento en la función `process_sensor()`.

### Resultado / Aprendizaje

* **Rechacé la alteración de firmas y renombramiento de clases:** La primera propuesta de la IA sobre-diseñaba la solución y renombraba la función **`process_sensor`** a **`process_sensor_data`**, rompiendo los contratos del evaluador. Exigí respetar al 100% las firmas del documento base.
* **Acepté el desacoplamiento SRP, OCP y LSP corregido:** Implementé el desacoplamiento de lectura física respecto a persistencia (S), el diseño polimórfico de alertas ampliando el sistema sin modificar el detector de anomalías (O), y la compatibilidad nominal de sensores (L), validándolo con una suite de **6 pruebas unitarias**.

---

## Prompt (Jueves)

> Completa la biblioteca en `semana1/solid_isp_dip.py` dividiendo una interfaz gorda en `Readable`, `Writable` y `Calibratable` (ISP), y usando `Protocol` para inyectar un `DataRepository` en un `DataProcessor` (DIP), junto con una implementación `InMemoryRepository` para pruebas.

### Respuesta

> Para prepararte de cara a la defensa con el coordinador, estructuramos `semana1/solid_isp_dip.py` con interfaces pequeñas (`Readable`, `Writable`, `Calibratable`) para no obligar a sensores analógicos simples a implementar métodos fantasma de calibración (ISP).
>
> En DIP, hacemos que `DataProcessor` dependa del protocolo `DataRepository` en su constructor. En producción le inyectas Postgres; en los tests le inyectamos `InMemoryRepository` en RAM. El procesador jamás se entera.

### Resultado / Aprendizaje

* **Acepté la segregación de interfaces con Protocol (ISP):** Evité acoplar dispositivos simples a clases monolíticas que los obliguen a heredar métodos vacíos o inoperantes de calibración y escritura.
* **Acepté el desacoplamiento de persistencia (DIP):** Implementé el protocolo **`DataRepository`** inyectando opcionalmente el repositorio simulado en memoria **`InMemoryRepository`** en el constructor de **`DataProcessor`**. Esto permitió probar la lógica en milisegundos en la RAM de forma aislada.

---

## Prompt (Viernes)

> Genera el código y los tests para el driver UART modular (`config`, `parsers`, `device`, `recorder`) aplicando principios SOLID según las firmas especificadas en la guía del curso.

### Respuesta

> ¡Freno de mano puesto, vaquero! Reestructuramos el plan para usar exactamente la arquitectura estipulada de **4 clases principales**:
>
> 1. `config.py` (`UartConfig`, dataclass inmutable con validaciones de hardware).
> 2. `parsers.py` (Contrato abstracto `MessageParser`, `ModbusParser` y `NMEAParser`).
> 3. `device.py` (`UartDevice` con inyección de dependencias para aislar la UART).
> 4. `recorder.py` (`DataRecorder` dedicado a persistir en formato `.jsonl`).

### Resultado / Aprendizaje

* **Rechacé el sobre-diseño de la IA con concurrencia compleja:** Descarté el buffer circular por exclusión mutua de hilos y *lockings* complejos sugerido por el asistente, simplificando el alcance para cumplir estrictamente con los 4 archivos dictados por la especificación.
* **Rechacé y corregí el comportamiento de `can_parse()` en `ModbusParser`:** La IA proponía arrojar un error de valor (`raise ValueError`) si la trama de entrada era corta. Identifiqué que esto rompía LSP y OCP al interrumpir toda la tubería de análisis polimórfica en cascada. Lo corregí para retornar limpiamente **`False`**.
* **Corregí la inyección de tipos nulos con Mypy:** Identifiqué que inyectar **`config=None`** en el test violaba la aserción nominal tipada **`config: UartConfig`**. Modifiqué el test para instanciar un objeto de configuración real, logrando el verde de tipos.


---

### Semana0.md


##### Prompts dados: 10

##### Chats creados: 1

---

## Prompt (Paso 1 - Configuración Inicial)

> **Hola, este chat está dedicado a la Semana 0 del curso. Estas son las instrucciones: Objetivo: que el lunes 13 de julio abras tu editor y estés listo para aprender, no para instalar. Todo esto es un checkpoint obligatorio que el coordinador verifica antes del arranque.**

> **Pasos (~4 horas en total):**
>
> 1. **Instala las herramientas base (60–90 min):** Python 3.12+, entorno virtual `.venv` del curso, y `pip install pytest pytest-cov ruff mypy fastapi uvicorn sqlalchemy alembic httpx`. Instala también Docker Desktop (se usa desde la semana 4, pero verificarlo hoy evita incendios): https://docs.docker.com/get-docker/ — Windows: usa WSL2.
> 2. **VS Code + GitHub Copilot (30 min):** instala VS Code (https://code.visualstudio.com/) con extensiones GitHub Copilot, Python, Pylance, GitLens y Ruff. Activa el plan Free de Copilot (sin tarjeta): https://github.com/features/copilot/plans — el plan Free tiene cupo mensual: adminístralo. Configura tu identidad de Git (`user.name`, `user.email`).
> 3. **Repositorio + curso (60 min):** crea el repositorio público `sdlc-electronica-[tu-nombre]` con README y `.gitignore` de Python, clónalo, y completa el curso interactivo "Introduction to GitHub" (~45 min): https://skills.github.com/.
> 4. **El checkpoint "hola-sensor" (45 min):** crea `semana0/hola_sensor.py` (clase `Sensor` con `read()` que devuelve `23.5`) y `semana0/test_hola_sensor.py`; ejecuta `pytest semana0/ -v` y haz commit: `"feat: checkpoint semana 0 - sensor minimo con test"`.
> 5. **Autodiagnóstico y presentación (15 min):** responde el formulario de autodiagnóstico y preséntate en el canal del grupo: quién eres, tu experiencia en electrónica y qué esperas del programa.
>
> **Checklist de cierre (entrega: domingo 12 de julio, 23:59):**
>
> * `python3`, `pytest`, `ruff` y `mypy` funcionan en tu terminal.
> * `docker --version` responde.
> * VS Code con Copilot activo (ícono visible).
> * Repositorio público creado y clonado, con el checkpoint `hola-sensor` y su test en verde.
> * Curso "Introduction to GitHub" completado (con el certificado del bot).
> * Autodiagnóstico enviado y presentación publicada en el canal.
> * Entrega en Classroom: el enlace a tu repositorio público.
>
> Si te atoras (WSL2, Docker, permisos), pide ayuda en el canal — la Semana 0 existe exactamente para resolver esto.

### Respuesta

> ¡Hola! Entendido. A partir de ahora asumo mi rol como tu asistente y compañero de estudio para el programa "De electrónica a desarrollo de software con IA", enfocándonos estrictamente en los objetivos de tu Semana 0.
>
> Como inteligencia artificial, mi objetivo es ayudarte a resolver cualquier bloqueo técnico de forma directa, empática y clara. La meta es que este domingo 12 de julio tengas todo tu checklist terminado y el lunes 13 puedas enfocarte al 100% en aprender a programar sin lidiar con problemas de instalación.
>
> ### Tu Misión para la Semana 0
>
> He registrado tus instrucciones. Aquí tienes el mapa mental de nuestro plan de ataque (estimado en ~4 horas):
>
> * **Paso 1 - Entorno Base:** Instalación de Python 3.12+, creación del entorno virtual `.venv` y configuración de dependencias clave (`pytest`, `ruff`, `fastapi`, `sqlalchemy`, etc.), además de dejar Docker Desktop listo (usando WSL2 si estás en Windows).
> * **Paso 2 - Editor e IA:** Configuración de VS Code con las extensiones necesarias y la activación de GitHub Copilot (plan Free) para potenciar tu escritura de código, junto con la configuración de tu identidad en Git.
> * **Paso 3 - Repositorio:** Creación de tu repositorio público `sdlc-electronica-[tu-nombre]`, clonación local y finalización del curso interactivo de GitHub Skills.
> * **Paso 4 - Checkpoint "hola-sensor":** Programar la clase `Sensor` en `semana0/hola_sensor.py`, escribir su prueba unitaria en `semana0/test_hola_sensor.py`, verificar que los tests pasen en verde y hacer tu commit.
> * **Paso 5 - Comunidad:** Llenado del autodiagnóstico y tu presentación en el canal del grupo.

### Resultado / Aprendizaje

* **Acepté la instalación guiada de Python 3.12+ y dependencias base:** Entendí la importancia de aislar las bibliotecas en el entorno virtual **`.venv`** para mantener un orden riguroso en las dependencias y preparar el entorno para evitar colisiones en futuras semanas.

---

## Prompt (Paso 1.1 - Inicio de Instalación)

> **Me encuentro en el paso 1, apenas descargué Python y Docker Desktop.**

### Respuesta

> ¡Excelente! Ya diste el primer gran paso. Descargar los instaladores suele ser la parte que da más pereza, pero ya tienes los cimientos. Como tu asistente de inteligencia artificial, te guiaré paso a paso para que todo quede perfectamente configurado y sin dolores de cabeza.
>
> Recuerda que tenemos hasta el domingo 12 de julio a las 23:59 para completar tu checklist, así que vamos con muy buen tiempo.
>
> Aquí tienes el plan de acción exacto para terminar el Paso 1:
>
> 1. Instalar Python de forma segura (Windows/macOS).
> 2. Crear tu entorno virtual del curso (`.venv`).
> 3. Instalar los paquetes (Dependencias): `pytest pytest-cov ruff mypy fastapi uvicorn sqlalchemy alembic httpx`.
> 4. Instalar Docker Desktop.

### Resultado / Aprendizaje

* **Acepté el plan de acción secuencial:** Inicié la instalación de los elementos esenciales de software e infraestructura (Docker) de forma ordenada y metódica.

---

## Prompt (Paso 1.2 - Bloqueo de Terminal en macOS)

> `salvaxtraw@MacBook-Air-de-Salvador SEMANA 0 % python -m venv .venv`
>
> `zsh: command not found: python`
>
> `salvaxtraw@MacBook-Air-de-Salvador SEMANA 0 % python -m venv .venv`
>
> `zsh: command not found: python`

### Respuesta

> ¡Hola! No te preocupes, este es un "incendio" clásico en macOS y tiene una solución muy sencilla.
>
> El error `zsh: command not found: python` ocurre porque en los sistemas Apple modernos, el comando `python` ya no viene vinculado por defecto. Para usar Python 3, debes llamarlo explícitamente como `python3`.
>
> Aquí tienes los pasos exactos para Mac:
>
> ```bash
> python3 --version
> python3 -m venv .venv
> source .venv/bin/activate
> pip install pytest pytest-cov ruff mypy fastapi uvicorn sqlalchemy alembic httpx
> ```

### Resultado / Aprendizaje

* **Corregí la llamada de comandos en macOS:** Solucioné la colisión del comando de terminal **`python`** usando el alias explícito de macOS **`python3`** para poder instanciar el entorno virtual de forma aislada.

---

## Prompt (Paso 1.3 - Dependencias instaladas)

> **yap, y ya instalé las dependencias, y el sistema que tengo es macOS.**

### Respuesta

> ¡Excelente! Superar la configuración del entorno virtual en macOS es una gran victoria. Ya tienes la base de Python lista.
>
> Para cerrar definitivamente el Paso 1, solo asegúrate de haber arrastrado Docker Desktop a tu carpeta de Aplicaciones, ejecútalo para levantar el daemon y verifica con:
>
> ```bash
> docker --version
> ```

### Resultado / Aprendizaje

* **Acepté la verificación final de Docker:** Comprobé de forma visual e instrumental que el daemon local de Docker responde correctamente en el terminal mediante **`docker --version`**.

---

## Prompt (Paso 2 - Confirmación)

> **Listo, continuemos.**

### Respuesta

> ¡Perfecto! Tener VS Code configurado con tu identidad de Git y la inteligencia artificial de Copilot activada es un antes y un después en la forma en la que escribirás código.
>
> Ahora vamos al Paso 3: Repositorio + curso. Aquí es donde conectaremos tu entorno local (tu Mac) con la nube de GitHub para que tu código esté respaldado y listo para entregar.

### Resultado / Aprendizaje

* **Acepté la preparación del editor:** Verifiqué que las extensiones clave de Python, Pylance, Ruff, GitLens y GitHub Copilot estuvieran correctamente instanciadas en VS Code.

---

## Prompt (Paso 3 - Curso completado)

> **Sip, y ya acabé el curso de GitHub.**

### Respuesta

> ¡Felicidades! Terminar el curso de GitHub Skills te da la base de control de versiones que usaremos en todo el programa. Ya estamos en la recta final.
>
> Ahora vamos al Paso 4: El checkpoint "hola-sensor". Este es tu primer reto de código y la prueba de fuego para confirmar que tu entorno (Python, pytest y Git) funciona perfectamente.

### Resultado / Aprendizaje

* **Acepté la finalización del curso "Introduction to GitHub":** Logré consolidar la base conceptual del control de versiones en Git y la gestión de ramas en la nube.

---

## Prompt (Paso 4.1 - Primer intento fallido de pytest)

> ```text
> (.venv) salvaxtraw@MacBook-Air-de-Salvador CURSO UV PROGRA % pytest semana0/ -v
> ============================================= test session starts ==============================================
> platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- /Users/salvaxtraw/CURSO UV PROGRA/.venv/bin/python3.14
> cachedir: .pytest_cache
> rootdir: /Users/salvaxtraw/CURSO UV PROGRA
> plugins: cov-7.1.0, anyio-4.14.1
> collected 0 items
> ============================================ no tests ran in 0.00s =============================================
> (.venv) salvaxtraw@MacBook-Air-de-Salvador CURSO UV PROGRA %
> ```

### Respuesta

> ¡Casi lo tenemos! La buena noticia aquí es que tu entorno virtual está activo y pytest funcionó a la perfección.
>
> El mensaje `collected 0 items` (0 elementos recolectados) significa que pytest buscó en la carpeta `semana0/` pero no encontró ningún archivo de pruebas.
>
> Esto es un clásico de la Semana 0 y suele pasar porque no guardaste los archivos en VS Code, por nombres incorrectos, o por estar posicionado en la carpeta equivocada (fuera del repositorio).

### Resultado / Aprendizaje

* **Corregí la estructura de carpetas y posicionamiento:** Identifiqué que estaba ejecutando los tests en una carpeta principal de pruebas en lugar de estar dentro de la raíz clonada de mi repositorio Git de producción.

---

## Prompt (Paso 4.2 - Error de Entorno Virtual Vacío)

> ```text
> salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % source /Users/salvaxtraw/sdlc-electronica-lyla_alice/semana0/.venv/bin/activate
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % pytest semana0/ -v
> zsh: command not found: pytest
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % python --version
> zsh: command not found: python
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % pytest semana0/ -v
> zsh: command not found: pytest
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % python3 --version
> Python 3.14.6
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % python3 -m venv .venv
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % pytest semana0/ -v
> zsh: command not found: pytest
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice %
> ```

### Respuesta

> ¡Ah! Veo exactamente lo que pasó. No te preocupes, este es un concepto súper importante que acabas de descubrir sobre los entornos virtuales.
>
> Estás en la carpeta correcta (`sdlc-electronica-lyla_alice`), e hiciste muy bien al crear el entorno virtual ahí con `python3 -m venv .venv`.
>
> ¿Por qué te dice `command not found: pytest`? Porque los entornos virtuales son "burbujas" aisladas. Las librerías que instalamos hace rato se quedaron en el entorno virtual de la otra carpeta. Este nuevo entorno que acabas de crear nació completamente vacío.
>
> Para solucionarlo, activa este nuevo entorno e instala las dependencias con `pip install`.

### Resultado / Aprendizaje

* **Acepté la reinstalación de dependencias en el entorno localizado:** Aprendí de forma empírica que cada entorno virtual es una burbuja aislada. Activé el **`.venv`** local e instalé la biblioteca de pruebas y de análisis estático desde la raíz de forma definitiva.

---

## Prompt (Paso 4.3 - ModuleNotFoundError en Pruebas)

> ```text
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % pytest semana0/ -v
> =================================================================== test session starts ===================================================================
> platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- /Users/salvaxtraw/sdlc-electronica-lyla_alice/.venv/bin/python3.14
> cachedir: .pytest_cache
> rootdir: /Users/salvaxtraw/sdlc-electronica-lyla_alice
> plugins: cov-7.1.0, anyio-4.14.1
> collected 0 items / 1 error
>
> ERROR collecting semana0/test_hola_sensor.py
>
> ImportError while importing test module '/Users/salvaxtraw/sdlc-electronica-lyla_alice/semana0/test_hola_sensor.py'.
> Hint: make sure your test modules/packages have valid Python names.
>
> Traceback:
> semana0/test_hola_sensor.py:2: in <module>
>     from semana0.hola_sensor import Sensor
> E   ModuleNotFoundError: No module named 'semana0'
>
> ================================================================= short test summary info =================================================================
> ERROR semana0/test_hola_sensor.py
> !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
> ==================================================================== 1 error in 0.04s ====================================================================
> ```

### Respuesta

> ¡Este es un excelente progreso! Tu entorno virtual y pytest están funcionando a la perfección. El error que estás viendo ya no es de instalación, es un error muy común de cómo Python lee los archivos.
>
> El mensaje dice: `ModuleNotFoundError: No module named 'semana0'`.
>
> Esto pasó porque tu asistente intentó importar el archivo usando el nombre de la carpeta, pero Python no sabe qué es `semana0` cuando se ejecuta desde adentro de la carpeta o sin un paquete formal.
>
> Cambia:
>
> `from semana0.hola_sensor import Sensor`
>
> por:
>
> `from hola_sensor import Sensor`.

### Resultado / Aprendizaje

* **Corregí el `ModuleNotFoundError` de pytest en la recolección de pruebas:** Identifiqué que el sistema de pytest requería una importación directa de los módulos dentro de la misma carpeta de trabajo (**`from hola_sensor import Sensor`** en lugar de **`from semana0.hola_sensor import Sensor`**), dejando la suite de pruebas del checkpoint inicial en verde brillante con **`1 passed`**.

---

## Prompt (Paso 5 - Cierre)

> **listo**

### Respuesta

> ¡Felicidades! Has superado oficialmente la parte técnica más pesada de toda la Semana 0. Lidiar con entornos virtuales, solucionar errores de importación y hacer tu primer push a la nube son habilidades fundamentales que usarás todos los días en tu transición al desarrollo de software.
>
> Ahora que tu código está seguro en GitHub y los tests pasan en verde, solo te falta el Paso 5 de autodiagnóstico y presentación para terminar tu checklist al 100% y poder entregar.

### Resultado / Aprendizaje

* **Acepté y completé el autodiagnóstico y presentación en la comunidad:** Compartí mis expectativas del programa y mi trasfondo en electrónica, cerrando con un **100% de cumplimiento** el checklist de inicio del Sprint 0.

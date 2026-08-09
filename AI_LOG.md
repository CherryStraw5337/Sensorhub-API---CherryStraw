# Bitácora de Inteligencia Artificial (AI_LOG.md)
**Herramienta utilizada:** Gemini 2.5 Pro

## Semana 1 · Entrada 1 (Lunes)
Prompt: "Mapea una lectura de sensor de C a Python moderno usando dataclasses inmutables, enums, tipado estructural (Protocol) y 5 funciones puras de procesamiento"
La IA propuso la estructura `Reading` con `@dataclass(frozen=True)`, el protocolo `Sensor` y las 5 funciones en `sensor_utils.py`. Acepté el código pero ajusté el flujo de validación:
- Acepté el modelado de datos y la sintaxis de reemplazo inmutable (`dataclasses.replace`), ya que elimina efectos secundarios comunes en punteros de C.
- Rechacé la forma inicial de ejecutar `mypy` desde dentro de la subcarpeta `semana1/` porque lanzaba errores de resolución de módulos. Lo corregí ejecutando las herramientas de auditoría siempre desde el directorio raíz del proyecto.

## Semana 1 · Entrada 2 (Martes)
Prompt: "Reimplementa una máquina de estados finita (FSM) orientada a objetos para experimentar el estilo OO frente al C procedural, con 4 tests unitarios"
La IA propuso inicialmente una FSM para un nodo IoT de sensores con manejo de excepciones complejas. Rechacé la primera propuesta y acepté la corrección:
- Rechacé el modelo de FSM IoT porque se desviaba de la especificación estricta de la guía, la cual pedía un semáforo (`TrafficLightFSM`).
- Acepté la segunda implementación con `TrafficLightState` y el uso de un diccionario para mapear las transiciones O(1) en lugar de un switch-case procedural.
- Acepté los 4 tests unitarios de `test_fsm.py` tras verificar que probaban exactamente los escenarios exigidos: estado inicial, transición RED->GREEN, ciclo completo y conteo de ciclos.

## Semana 1 · Entrada 3 (Miércoles)
Prompt: "Implementa los tres primeros principios SOLID (S, O y L) con el código base y las firmas exactas indicadas en la guía para SensorReader, AlertStrategy, AnomalyDetector y process_sensor"
La IA propuso inicialmente una versión sobre-diseñada (over-engineered) que renombraba métodos (como `process_sensor_data`), cambiaba firmas de clases e ignoraba las interfaces explícitas entregadas en la guía. Rechacé esa primera propuesta y exigí una corrección estricta:
- Rechacé la modificación de firmas y el renombramiento de clases base. En arquitectura de software, alterar un contrato preestablecido rompe la compatibilidad e invalida pruebas automatizadas de integración.
- Acepté la implementación corregida tras auditar que preservaba intacto el fragmento de la guía (`AlertStrategy`, `AnomalyDetector`, `process_sensor`), limitándose únicamente a construir las clases derivadas (`ConsoleAlert`, `FileAlert`, `TemperatureSensor`, `HumiditySensor`) y los ejemplos de contraste "mal/bien".
- Acepté los 6 tests unitarios correspondientes (2 por cada principio) tras verificar su paso exitoso en pytest.

## Semana 1 · Entrada 4 (Jueves)
Prompt: "Completa la biblioteca en semana1/solid_isp_dip.py dividiendo una interfaz gorda en Readable, Writable y Calibratable (ISP), y usando Protocol para inyectar un DataRepository en un DataProcessor (DIP), junto con una implementación InMemoryRepository para pruebas"
La IA generó las estructuras de los protocolos y las clases de prueba sin alterar el fragmento base proporcionado en la guía. Acepté la implementación tras verificar línea por línea:
- Acepté la segregación de interfaces con `Protocol` (ISP), ya que evita que dispositivos de solo lectura como un ADC implementen métodos fantasma de calibración o escritura.
- Acepté el patrón de Inversión de Dependencias (DIP) y la clase `InMemoryRepository`. Comprobé que al inyectar la dependencia vía parámetro en `DataProcessor`, podemos testear toda la lógica de procesamiento en memoria RAM en milisegundos sin depender de conexiones a bases de datos externas.
- Acepté los 4 tests unitarios elaborados en `test_solid_isp_dip.py` tras validar que pasan limpiamente en pytest y cubren tanto el éxito como el manejo de lecturas inexistentes (`None`).

## Semana 1 · Entrada 5 (Viernes)
Prompt: "Genera el código y los tests para el driver UART modular (config, parsers, device, recorder) aplicando principios SOLID según las firmas especificadas en la guía del curso"
La IA propuso inicialmente una arquitectura con extensiones complejas (como buffers circulares por mutex y loggers JSON) que se desviaban de los archivos requeridos en la especificación. Rechacé la primera propuesta y obligué a una alineación estricta, detectando además un bug crítico en la lógica de evaluación. Igualmente, modifiqué los tests otorgados para separarlos y aplicarles una mejor estructura:
- **Rechacé el sobre-diseño arquitectónico:** Reduje el alcance para implementar únicamente los 4 archivos dictados por la guía (`config.py`, `parsers.py`, `device.py`, `recorder.py`).
- **Rechacé y corregí el comportamiento de `can_parse()` en `ModbusParser`:** La IA sugirió lanzar una excepción (`raise ValueError`) si la trama era corta. Esto violaba el Principio de Sustitución de Liskov (LSP) y Abierto/Cerrado (OCP), ya que colgaría la tubería de análisis completa si un coordinador tuviera múltiples parsers en cadena. Lo corregí para retornar `False`.
- **Acepté las firmas de los 12 tests unitarios básicos** tras comprobar que cubren los criterios mínimos exigidos (baudrates inválidos, inmutabilidad y persistencia).

****

## Semana 2 · Entrada 1 (Lunes)
Prompt: "Ayúdame a completar mis notas de la Scrum Guide 2020 con los 5 eventos y sus timeboxes, los 3 artefactos con sus compromisos, los 5 valores y la diferencia entre Definition of Done y Criterio de Aceptación, manteniendo estrictamente mi estilo de escritura y terminología en inglés"
La IA propuso el bloque de texto exacto para insertar en mi archivo Markdown, respetando el formato de viñetas y sin agregar burocracia innecesaria. Acepté las definiciones teóricas pero aclaramos la arquitectura de integración del tablero ágil:
- **Acepté la conceptualización técnica de los artefactos y sus compromisos asociados** (Product Goal, Sprint Goal y Definition of Done), así como la distinción clara entre DoD como estándar global de calidad para todo el producto y Criterio de Aceptación como condición funcional específica en Gherkin para una sola User Story.
- **Rechacé la duda inicial de crear el GitHub Project como un proyecto o repositorio aislado:** Tras analizar la diferencia arquitectónica entre un repositorio de código (Repo - control de versiones e historial inmutable) y un tablero ágil (Project - capa de gestión visual superpuesta al SDLC), determiné con criterio propio que integrarlo dentro del mismo repositorio es la mejor práctica en la industria para vincular de forma nativa los Issues con los futuros Pull Requests.

## Semana 2 · Entrada 2 (Martes)
Prompt: "Audita como un ingeniero implacable mi borrador de 7 User Stories con escenarios Gherkin para un sistema de monitoreo IoT de bodega industrial. Señala ambigüedades, casos borde olvidados para TDD y ayúdame a reestructurar el backlog hasta superar las 10 historias con priorización MoSCoW y Story Points en escala Fibonacci"
La IA propuso una auditoría técnica profunda que expuso varios fallos de diseño en mi borrador inicial y sugirió reestructurar el Product Backlog a 11 historias. Acepté las correcciones arquitectónicas y ajusté los límites de frontera para el diseño de pruebas:
- **Acepté la corrección del rol del actor**, cambiando "Como desarrolladora..."por usuarios funcionales de negocio ("Como administradora de bodega"), ya que en el SDLC el software se construye para aportar valor operativo en tiempo de ejecución, no para quien escribe el código.
- **Acepté la eliminación de "cadenas mágicas"** (Magic Strings, como hardcodear el ID "GHOST_99" en las pruebas) por condiciones dinámicas de inventario, y la integración de la historia US-08 para aplicar el patrón Strategy en el AlertManager (salida dual a consola y archivo) exigido por la rúbrica.
- **Rechacé y corregí el comportamiento de mi diseño inicial en la US-03**, donde indicaba abrir el log de problemas en "modo lectura". Arquitectónicamente, ante una excepción o superación del límite de sensores, el sistema debe escribir en la bitácora (modo append), no leerla.
- **Corregí la ambigüedad en los umbrales de temperatura y humedad para habilitar un TDD estricto**, definiendo explícitamente el comportamiento en las fronteras matemáticas (qué ocurre exactamente a los 35.0 °C) e introduciendo un caso borde de física imposible (-5 K) en la US-05 para verificar el manejo robusto de excepciones de dominio.

## Semana 2 · Entrada 3 (Miércoles)
Prompt: "Guíame paso a paso para implementar SensorRegistry, AnomalyDetector y AlertManager siguiendo un ciclo TDD estricto (Red-Green-Refactor), aplicando inyección de dependencias para umbrales y el patrón Strategy para las alertas"
La IA propuso los ciclos atómicos de prueba y código para cada componente, asegurando que las pruebas fallaran primero (RED) antes de implementar la lógica mínima (GREEN). Acepté la estructura pero realicé ajustes operativos en el entorno:
- **Acepté el diseño arquitectónico:** Validé el uso de inyección de dependencias en `AnomalyDetector` (evitando hardcodear 35.0 °C o 80.0 %) y el patrón Strategy mediante `Protocol` en `AlertManager`. Esto me permitió alcanzar un 99% de cobertura en las pruebas automatizadas.
- **Rechacé y corregí el flujo de ejecución de pruebas:** Al inicio, la ejecución directa de `pytest` falló arrojando un `ModuleNotFoundError`. Analicé que el `PYTHONPATH` no estaba resolviendo la raíz del proyecto; lo corregí creando los archivos `__init__.py` necesarios y adoptando el comando estándar `python -m pytest` para todo el ciclo.
- **Corregí hallazgos de análisis estático en el Refactor:** Durante los ciclos en verde, ejecuté `ruff check` y detecté importaciones huérfanas introducidas por los ejemplos de la IA (como un `import pytest` sin uso en `test_detector.py`). Acepté el fallo del linter y limpié las dependencias antes de sellar el commit de refactorización.

## Semana 2 · Entrada 4 (Jueves)
Prompt: "Ayúdame a redactar la Definition of Done estricta, configurar pyproject.toml para automatizar la calidad (cobertura >= 80%, ruff, mypy) y generar los artefactos Scrum finales (Sprint Planning y Retrospective) basados en nuestro historial"
La IA generó el contrato en `DEFINITION_OF_DONE.md`, el archivo de configuración para centralizar las reglas de validación en Python, y los textos de los artefactos Scrum, sugiriendo integrar los cambios mediante ramas. Acepté la implementación tras verificar su impacto en el proyecto:
- **Acepté la automatización del contrato de calidad:** Validé la configuración en `pyproject.toml` (`--cov-fail-under=80`, `strict=true` para mypy). Reflexioné que como ingeniero es ineficiente auditar estilos o cobertura a mano; delegar estas reglas a un sistema automatizado (CI local) asegura que los tests fallen si se viola la DoD.
- **Acepté la integración mediante flujo Git profesional:** Adopté la recomendación de encapsular la configuración en una rama aislada (`feature/config-dod`) y simular un Pull Request local hacia `main`. Aunque trabajo solo, esto mantiene un historial limpio y respeta el estándar corporativo.
- **Validé los artefactos Scrum con criterio propio:** Revisé el *Sprint Planning* asegurando que las tareas mantuvieran el rigor heurístico de $\le 4$ horas, y definí en la *Retrospectiva* una acción de mejora real: implementar un checklist de *scaffolding* para prevenir los problemas de entorno (`ModuleNotFoundError`) sufridos el día anterior.

## Semana 2 · Entrada 5 (Viernes)
Este día no cuenta con entrada ya que se trabajó los 4 días anteriores en el proyecto, por ende no se realizó ninguna modificación este día.

****

## Semana 3 · Entrada 1 (Lunes)
Prompt: "Acompáñame a estructurar la capa inicial de presentación (routers) con FastAPI, definiendo modelos Pydantic estrictos, reconfigurando mis herramientas de calidad en pyproject.toml para analizar el nuevo paquete app/ y aplicando un commit por archivo."
La IA propuso los comandos y el código necesario para establecer la estructura base del producto (app/), el contrato de datos y un endpoint inicial "mockeado". Acepté el diseño base pero reflexioné activamente sobre los mecanismos de protección de la API y la estrategia de versionado:
- **Acepté la arquitectura orientada a producto y los contratos Pydantic:** Comprendí que mudar el desarrollo de carpetas de ejercicios a un paquete raíz (app/) con `__init__.py` es el paso crítico para un despliegue en la nube. Validé que usar Pydantic para definir entradas `(SensorReadingIn)` actúa exactamente como un validador de tramas de hardware, rechazando peticiones malformadas (como enviar un string en lugar de un float de temperatura) devolviendo un código 422 `(Unprocessable Entity)` sin que el sistema gaste recursos de procesamiento.
- **Acepté el flujo de control de dependencias:** Rechacé depender de un pip freeze generado automáticamente que incluiría dependencias transitivas (ruido) y, en su lugar, acepté la práctica de curar manualmente el `requirements.txt` en la raíz.
- **Acepté y ejecuté la integración mediante Commits Atómicos:** Implementé una estrategia de control de versiones aislando el trabajo del día en una rama `(feature/semana-3-dia-1)` y realizando commits individuales y atómicos por cada archivo modificado (e.g., `pyproject.toml`, `requirements.txt`, `app/main.py`), finalizando con un merge limpio hacia main para facilitar futuras revisiones por pares `(peer reviews)`.

## Semana 3 · Entrada 2 (Martes)
Prompt: "Configura la persistencia con SQLAlchemy 2.0 usando la sintaxis Mapped para ReadingModel y SensorModel, replicando el dominio de la semana 2 con una relación relacional." 
La IA propuso la configuración del motor (engine) y la base de datos local SQLite. Acepté la implementación tras corregir la lógica de normalización y el manejo de tiempo:
- **Acepté la normalización relacional:** Inicialmente la IA propuso un modelo plano. Corregí el diseño para implementar una relación 1:N (Un Sensor tiene muchas Lecturas), definiendo SensorModel como la tabla maestra de configuración y ReadingModel con una llave foránea (ForeignKey), ahorrando redundancia de datos
- **Acepté el uso de la API tipada de SQLAlchemy 2.x:** Utilicé Mapped y mapped_column para asegurar que los modelos sean compatibles con mypy, actuando de forma tan estricta como un struct en C
- **Corregí el manejo de fechas:** La IA sugirió utcnow(), el cual está deprecado en Python 3.12+. Cambié la implementación a datetime.now(timezone.utc) para garantizar la compatibilidad con el ecosistema moderno

## Semana 3 · Entrada 3 (Miércoles)
Prompt: "Implementa el patrón repositorio y la capa de servicio para lecturas, aplicando Inversión de Dependencias (DIP) mediante protocolos y validando la lógica con un repositorio fake en memoria." 
La IA propuso la separación de responsabilidades y los ciclos de prueba para el servicio. Acepté la arquitectura tras resolver fallos críticos de inicialización:
- **Acepté el desacoplamiento mediante DIP:** Validé el uso de ReadingRepository(Protocol). Esto permite que el servicio sea agnóstico a la infraestructura, pudiendo testear la lógica de negocio en milisegundos usando un FakeReadingRepository en RAM sin tocar el disco duro.
- **Rechacé y corregí el fallo de registro de modelos:** Al ejecutar los tests, surgió un InvalidRequestError porque SQLAlchemy no encontraba el nombre '`SensorModel'`. Identifiqué que se debía a una importación perezosa; corregí el problema forzando la precarga de todos los modelos en `app/models/__init__.py`
- **Acepté el incremento parcial de cobertura:** Logré un 62.69% de cobertura testeando la capa de servicio en aislamiento, comprendiendo que el 80% final llegaría tras cablear los routers el jueves

## Semana 3 · Entrada 4 (Jueves)
Prompt: "Conecta las capas con inyección de dependencias en FastAPI (Depends) y diseña los endpoints REST para lecturas incluyendo paginación y filtros por fecha." 
La IA generó la estructura de los routers y la integración final. Acepté la propuesta pero realicé una corrección arquitectónica vital en la suite de pruebas:
- **Acepté el uso de APIRouter y Depends:** Implementé la inyección de la sesión de base de datos (`get_db`) y del servicio de forma modular, permitiendo que cada endpoint declare sus necesidades de forma limpia.
- **Rechacé y corregí el fallo de persistencia en los tests:** Los tests de integración fallaban con `OperationalError: no such table: readings`. Descubrí que el `TestClient` abría conexiones nuevas que entregaban bases de datos en memoria vacías. Corregí esto implementando `StaticPool` en `tests/test_api.py` para forzar una única conexión compartida durante toda la prueba.
- **Validé el cumplimiento de la meta de calidad:** Con el cableado completo y los tests de integración, alcancé una cobertura del 89.38%, superando el estándar esperado del 80%.

## Semana 3 · Entrada 5 (Viernes)
Prompt: "Implementa el ejercicio integrador de SensorHub con arquitectura de 4 capas completa y validación física real que rechace valores fuera de rango según la configuración del sensor en la base de datos." 
La IA propuso los repositorios y servicios finales para sensores y lecturas. Acepté la implementación tras un proceso de depuración técnica intensivo por inconsistencias de tipado:
- **Acepté la "Validación Física Real":** El servicio ahora compara cada lectura contra el min_value y max_value configurados en la tabla de sensores. Comprobé mediante tests que el sistema rechaza unidades incorrectas `(error 400)` y valores imposibles `(error 422)`, actuando como un circuito de protección de hardware en software.
- **Rechacé y corregí el tipado estricto para `Mypy`:** La IA inicialmente no manejó correctamente el retorno de SQLAlchemy 2.0 `(Sequence)`. Corregí manualmente 36 errores de `mypy` aplicando casting explícito a `list()` y definiendo todas las anotaciones de retorno faltantes `(no-untyped-def)`.
- **Corregí incompatibilidades de Python 3.14:** Debido al uso de una versión experimental de Python, las dependencias inyectadas con valores por defecto lanzaban un `TypeError`. Corregí el error migrando toda la inyección de dependencias de los routers a la sintaxis moderna con `Annotated`, blindando el sistema para el futuro.

***

## Semana 4 · Entrada 1 (Lunes)
Prompt: "Conteneriza mi aplicación FastAPI con un `Dockerfile` optimizado utilizando una imagen base ligera y aprovechando el caché de capas para las dependencias."
La IA propuso un Dockerfile estándar de una sola etapa. Acepté la lógica pero realicé ajustes para alcanzar el nivel de Alto Potencial:
- **Acepté el uso de `python:3.12-slim`:** Redujimos el peso de la imagen y mejoramos la seguridad eliminando herramientas de sistema innecesarias.
- **Corregí el orden de las capas:** Aseguré que el `COPY requirements.txt` preceda al `COPY . .` para que los cambios en el código no obliguen a reinstalar todas las librerías, optimizando el tiempo de construcción de minutos a segundos.

## Semana 4 · Entrada 2 (Martes)
Prompt: "Orquesta la API y una base de datos PostgreSQL 16 usando Docker Compose, y configura Alembic para que la conexión a la base de datos sea dinámica según el entorno."
La IA generó el archivo `docker-compose.yml` y la configuración de Alembic. Realicé auditorías críticas sobre la conectividad:
- **Acepté la normalización de la URL en `db.py`:** Implementamos `get_database_url()` para manejar automáticamente el prefijo `postgresql+psycopg://`, evitando errores de driver comunes en despliegues.
- **Corregí un conflicto de puertos:** Mi máquina local ya tenía un proceso de Postgres ocupando el puerto 5432. Modifiqué la orquestación para exponer el servicio en el 5433 hacia el host sin romper la red interna de Docker.

## Semana 4 · Entrada 3 (Miércoles)
Prompt: "Configura un pipeline de Integración Continua (CI) en GitHub Actions que ejecute Ruff, Mypy y Pytest con una cobertura mínima del 80%."
La IA generó el archivo `ci.yml`. Ejecutamos un ciclo real de RED-GREEN-REFACTOR:
- **Acepté el bloqueo de seguridad:** El pipeline falló inicialmente (RED) debido a errores de estilo detectados por Ruff.
- **Corregí y saneé el código:** Utilicé `ruff check --fix` localmente para resolver las fallas antes de lograr el check verde (GREEN) y añadí el badge de estado al `README.md`.

## Semana 4 · Entrada 4 (Jueves)
Prompt: "Implementa un Health Check endpoint usando TDD y configura la infraestructura como código en `Render.com` mediante `render.yaml`."
La IA sugirió la estructura del endpoint y el archivo de Blueprint. Apliqué rigor técnico en la implementación:
- **Acepté el flujo TDD:** Escribí primero el test que fallaba (RED) antes de crear la ruta `/health` en `main.py` (GREEN).
- **Acepté la automatización de migraciones:** Configuré el comando de arranque para ejecutar `alembic upgrade head` antes de iniciar el servidor, garantizando que el esquema de base de datos exista antes de recibir tráfico en producción.

## Semana 4 · Entrada 5 (Viernes)
**Este día es especial ya que tiene dos etapas**

Prompt: "Diagnostica el error '`OperationalError: no such table`' en el despliegue de Render y soluciona el conflicto de historias para permitir el Pull Request desde una rama huérfana."
La IA identificó problemas en la carga de modelos en Alembic y la desconexión entre ramas. Tomé decisiones críticas de cierre:
- **Corregí la configuración de `env.py`:** Importé manualmente los modelos (`SensorModel`, `ReadingModel`) para que la autogeneración de Alembic detectara las tablas físicas, resolviendo la falla en la nube.
- **Resolví el bloqueo de Git:** Dado que `semana4` era una rama huérfana, GitHub no permitía el PR. Forcé la vinculación de historias mediante `git merge main --allow-unrelated-histories` para habilitar el flujo de Despliegue Continuo (CD) exigido en la rúbrica.

Prompt: "Ayúdame a corregir el código de mis repositorios Fake. Al correr Mypy me está arrojando este error: `Argument 2 to "ReadingService" has incompatible type "FakeSensorRepository"; expected "SensorRepository" [arg-type]`"
(Tras el primer ajuste) "Mypy ahora arroja: `Incompatible types in assignment (expression has type "FakeSensorRepository", variable has type "SensorRepository")`"
La IA diagnosticó dos problemas fundamentales en mis simuladores de base de datos. Primero, discrepancias en las firmas de los métodos (uso de `Any` en lugar de esquemas Pydantic, y variables sueltas en lugar de `SensorUpdate`). Segundo, identificó que Mypy aplica **Subtipado Nominal** por defecto; por lo tanto, aunque los métodos coincidieran, Mypy bloqueaba la ejecución porque `FakeSensorRepository` no tenía un parentesco formal (herencia) con la clase `SensorRepository` que exigía el servicio.
Ésta vez, las desiciones fueron tomadas tras ser pasadas por un repo de prubea:

- **Alineación estricta de contratos:** Refactoricé los repositorios *Fake* para que utilicen exactamente los mismos modelos de Pydantic (`SensorCreate`, `SensorUpdate`) y nombren sus métodos idéntico a la capa de persistencia real (`get_all` en lugar de `list_all`).
- **Herencia Estratégica para Mypy:** Hice que mis repositorios simulados heredaran formalmente de las clases originales (`class FakeSensorRepository(SensorRepository):`).
- **Desacoplamiento en Unit Tests:** Sobrescribí el método `__init__` de los Fakes (evitando llamar a `super().__init__(session)`) para no requerir la conexión a la base de datos de SQLAlchemy durante las pruebas. Esto resolvió el chequeo estricto de tipos al 100%, manteniendo las pruebas rápidas, aisladas y respetando el Principio de Inversión de Dependencias (DIP).
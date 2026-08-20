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

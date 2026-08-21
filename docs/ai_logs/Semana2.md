# **Semana 2 - Scrum, TDD y User Stories**

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

````
* **Acepté:** El diseño arquitectónico completo con inyección de dependencias en `AnomalyDetector` [20, 23] y el patrón Strategy mediante `Protocol` en `AlertManager` [20, 24]. Esto nos permitió alcanzar un **99% de cobertura total** de la suite de pruebas [25].
* **Rechacé y Corregí:** El primer error de entorno al correr pytest (`ModuleNotFoundError: No module named 'semana2'`) [26]. Identifiqué que el PYTHONPATH local de macOS no estaba mapeando la carpeta raíz [27]. Lo corregí usando el comando estandarizado `python -m pytest` y añadiendo los archivos de inicialización `__init__.py` necesarios en cada nivel para habilitar la importación jerárquica [27-30].
* **Corregí:** Un fallo de análisis estático en el Refactor del ciclo 3, donde la IA sugirió un `import pytest` redundante en `test_detector.py` [20, 31]. Al correr `ruff check .` detectamos la importación inútil y la eliminamos para mantener un código limpio antes de sellar el commit [20, 31].

---

#### Jueves · Entrada 4 (DoD y Calidad Automatizada)
`````

### #### Jueves · Entrada 4 (DoD y Calidad Automatizada)

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

# User Stories - Semana 3 a 5

## US-01: Verificar y registrar conexión de sensor nuevo

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `2`

> Como administradora de bodega, quiero que el sistema detecte y registre automáticamente cualquier sensor nuevo que se conecte, para mantener un inventario actualizado de los dispositivos de monitoreo en la planta.

### Scenario: Registro exitoso de sensor nuevo

* **Given:** un sensor con ID `TEMP_01` que no está registrado en el sistema.
* **When:** el sensor envía su paquete de inicialización y handshake.
* **Then:** el sistema lo registra en el inventario activo con estado `OK`.
* **And:** el dispositivo queda disponible para consulta en el historial de conexiones.

### Scenario: Reconexión de sensor ya existente

* **Given:** un sensor con ID `TEMP_01` que ya existe en el registro del sistema.
* **When:** el sensor envía su paquete de inicialización tras un reinicio.
* **Then:** el sistema restablece su sesión con estado `OK` sin duplicar el registro.
* **And:** se registra el evento de reconexión en el historial.

---

## US-02: Categorización automática por tipo de medición

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `3`

> Como administradora de bodega, quiero que el sistema clasifique los sensores automáticamente según sus unidades de medición desde su primer payload, para asignarles las reglas de validación y almacenamiento correctas sin tiempos de espera.

### Scenario: Categorización de sensor de temperatura

* **Given:** un sensor recién conectado que envía un payload de prueba.
* **When:** el payload incluye la unidad de medición en `C`, `F` o `K`.
* **Then:** el sistema clasifica el sensor en la categoría `TEMPERATURE`.
* **And:** le asigna el identificador estándar correspondiente (ej. `TEMP_01`).

### Scenario: Categorización de sensor de humedad

* **Given:** un sensor recién conectado que envía un payload de prueba.
* **When:** el payload incluye la unidad de medición en `%H`.
* **Then:** el sistema clasifica el sensor en la categoría `HUMIDITY`.
* **And:** le asigna el identificador estándar correspondiente (ej. `HUM_01`).

### Scenario: Rechazo de sensor con unidades desconocidas

* **Given:** un sensor recién conectado que envía un payload de prueba.
* **When:** el payload incluye unidades no soportadas (ej. `LUMENS` o `PSI`).
* **Then:** el sistema rechaza la conexión con el estado `UNSUPPORTED_TYPE`.
* **And:** elimina el dispositivo del registro temporal.

---

## US-03: Validación estricta de 10 sensores activos

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `5`

> Como administradora de bodega, quiero que el monitoreo solo inicie cuando haya exactamente 10 sensores calibrados y activos, para garantizar la cobertura térmica y de humedad completa en toda la superficie industrial.

### Scenario: Inicio exitoso con exactamente 10 sensores

* **Given:** que existen exactamente 10 sensores registrados y activos en el sistema.
* **When:** el sistema inicia el ciclo de monitoreo continuo.
* **Then:** el estado general cambia a `MONITORING_ACTIVE`.
* **And:** el motor de ingesta comienza a procesar lecturas cada 30 segundos.

### Scenario: Bloqueo por déficit de sensores (Menos de 10)

* **Given:** que hay 9 o menos sensores activos en el sistema.
* **When:** se intenta iniciar el ciclo de monitoreo continuo.
* **Then:** el sistema lanza una excepción `InsufficientSensorsException`.
* **And:** el monitoreo permanece en estado `STOPPED`.
* **And:** se escribe el error de déficit de cobertura en el archivo `problemlog.md`.

### Scenario: Bloqueo por exceso de sensores (Más de 10)

* **Given:** que hay 11 o más sensores enviando tramas al sistema.
* **When:** se intenta iniciar el ciclo de monitoreo continuo.
* **Then:** el sistema lanza una excepción `LimitExceededException`.
* **And:** el monitoreo permanece en estado `STOPPED`.
* **And:** se escribe el error de sobrecapacidad en el archivo `problemlog.md`.

---

## US-04: Control de tasa de muestreo (Rate Limiting de 30s)

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `3`

> Como administradora de bodega, quiero limitar la recepción de datos de cada sensor a una lectura máximo cada 30 segundos, para evitar la saturación de la base de datos y filtrar ruidos por envíos compulsivos del hardware.

### Scenario: Lectura aceptada respetando el intervalo

* **Given:** que el sensor `TEMP_01` realizó su última lectura hace 30 segundos o más.
* **When:** envía una nueva lectura válida al sistema.
* **Then:** la lectura se procesa y se almacena en el historial con estado `OK`.

### Scenario: Lectura descartada por frecuencia excesiva (Spamming)

* **Given:** que el sensor `TEMP_01` realizó su última lectura hace 12 segundos.
* **When:** envía una nueva lectura al sistema.
* **Then:** la lectura es descartada por el limitador de frecuencia.
* **And:** se almacena un registro de evento descartado con estado `RATE_LIMIT_EXCEEDED`.
* **And:** no se altera el timestamp de la última lectura válida.

---

## US-05: Normalización y conversión de temperaturas a Celsius

**Etiqueta:** `MoSCoW: Should`
**Story Points:** `2`

> Como administradora de bodega, quiero que todas las mediciones térmicas en Fahrenheit o Kelvin se conviertan automáticamente a Celsius antes de procesarse, para estandarizar las comparaciones con los umbrales de anomalía del negocio.

### Scenario: Conversión exitosa desde Fahrenheit

* **Given:** una lectura recibida de `TEMP_02` con un valor de `95.0` y unidad `F`.
* **When:** pasa por el módulo de normalización de datos.
* **Then:** el valor se transforma exactamente a `35.0` con unidad `C`.
* **And:** se almacena en el historial como `35.0 °C`.

### Scenario: Conversión exitosa desde Kelvin

* **Given:** una lectura recibida de `TEMP_03` con un valor de `308.15` y unidad `K`.
* **When:** pasa por el módulo de normalización de datos.
* **Then:** el valor se transforma exactamente a `35.0` con unidad `C`.
* **And:** se almacena en el historial como `35.0 °C`.

### Scenario: Rechazo de valor físicamente imposible en Kelvin (Caso borde TDD)

* **Given:** una lectura recibida de `TEMP_03` con un valor de `-5.0` y unidad `K`.
* **When:** pasa por el módulo de normalización de datos.
* **Then:** el sistema rechaza la medición lanzando un `InvalidPhysicalValueException`.
* **And:** la lectura se registra con estado `ERR_OUT_OF_BOUNDS`.

---

## US-06: Validación de integridad del payload de lectura

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `3`

> Como administradora de bodega, quiero verificar que los paquetes de datos recibidos contengan formatos numéricos válidos y estén dentro del rango físico del sensor, para prevenir caídas del sistema por datos corruptos o cortocircuitos.

### Scenario: Payload íntegro y dentro de rango

* **Given:** el sensor `HUM_01` envía una lectura de `45.5%` con timestamp UTC válido.
* **When:** el sistema valida la estructura del mensaje.
* **Then:** la lectura se marca con estado `OK` y se pasa al detector de anomalías.

### Scenario: Payload con datos corruptos (No numérico)

* **Given:** un sensor envía una trama donde el valor de lectura es la cadena `ERROR_READ`.
* **When:** el sistema intenta parsear el valor flotante.
* **Then:** se captura un error de conversión y la lectura se marca como `ERR_CORRUPT_PAYLOAD`.
* **And:** el evento se registra en la bitácora de problemas.

### Scenario: Lectura fuera de rango físico del sensor (Hardware Fault)

* **Given:** el sensor `TEMP_01` envía una lectura de `450.0 °C`.
* **When:** el sistema compara el valor con los límites de operación del hardware (`-50` a `100 °C`).
* **Then:** la lectura se descarta por fallo de sensor y se marca como `ERR_HARDWARE_FAULT`.

---

## US-07: Detección de anomalías térmicas y de humedad con alerta en consola

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `5`

> Como administradora de bodega, quiero que el sistema evalúe cada lectura normalizada contra los umbrales de seguridad y emita una alerta visual en consola al superarlos, para que los operadores reaccionen de inmediato ante riesgos en la mercancía.

### Scenario: Umbral de temperatura superado (Anomalía detectada)

* **Given:** un sensor `TEMP_01` que registra una lectura normalizada de `35.1 °C`.
* **And:** un detector configurado con el umbral límite inyectado de `35.0 °C`.
* **When:** la lectura es evaluada por el `AnomalyDetector`.
* **Then:** se genera un evento de anomalía con severidad `WARNING`.
* **And:** el `AlertManager` imprime el mensaje `ALERTA: TEMP_THRESHOLD_BREACHED en TEMP_01 [35.1 °C]` en la consola.

### Scenario: Umbral de humedad superado (Anomalía detectada)

* **Given:** un sensor `HUM_01` que registra una lectura de `80.5 %`.
* **And:** un detector configurado con el umbral límite inyectado de `80.0 %`.
* **When:** la lectura es evaluada por el `AnomalyDetector`.
* **Then:** se genera un evento de anomalía con severidad `WARNING`.
* **And:** el `AlertManager` imprime el mensaje `ALERTA: HUM_THRESHOLD_BREACHED en HUM_01 [80.5 %]` en la consola.

### Scenario: Valor en el límite exacto no genera alerta (Caso borde TDD estricto)

* **Given:** un sensor `TEMP_01` que registra una lectura normalizada de exactamente `35.0 °C`.
* **When:** la lectura es evaluada por el `AnomalyDetector`.
* **Then:** no se genera ninguna anomalía.
* **And:** el sistema clasifica la medición con estado `NORMAL`.

---

## US-08: Estrategia de persistencia de alertas en archivo de bitácora

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `3`

> Como administradora de bodega, quiero que todas las alertas de anomalías también se escriban en un archivo persistente del sistema, para mantener un historial de incidentes auditable a largo plazo sin depender de la consola.

### Scenario: Escritura de alerta en archivo log

* **Given:** el `AlertManager` tiene configurada la estrategia de salida `FileAlertStrategy` apuntando a `alerts.log`.
* **When:** se activa una alerta de tipo `TEMP_THRESHOLD_BREACHED` para el sensor `TEMP_01`.
* **Then:** el sistema añade una nueva línea al archivo `alerts.log` con el timestamp exacto, ID del sensor y valor medido.
* **And:** el archivo conserva las alertas anteriores sin sobrescribirlas (modo append).

### Scenario: Fallo de escritura en disco sin detener la aplicación

* **Given:** que el archivo `alerts.log` está bloqueado o sin permisos de escritura.
* **When:** el `AlertManager` intenta escribir una nueva alerta en el disco.
* **Then:** se captura una excepción de E/S (`IOException`).
* **And:** el sistema redirige la alerta a la salida de emergencia en consola sin interrumpir el monitoreo.

---

## US-09: Simulación de lecturas con distribución gaussiana (Extensión Alto Potencial)

**Etiqueta:** `MoSCoW: Could`
**Story Points:** `8`

> Como administradora de bodega, quiero disponer de un simulador de sensores que genere datos sintéticos usando una distribución normal (gaussiana), para probar el rendimiento del sistema de monitoreo y las alertas bajo condiciones de operación realistas sin hardware conectado.

### Scenario: Generación de lecturas en rango normal

* **Given:** un `SensorSimulator` configurado con media de `22.0 °C` y desviación estándar de `2.0 °C`.
* **When:** se ejecutan 60 ciclos de simulación.
* **Then:** el 95% de las lecturas generadas se mantienen dentro del rango de `18.0 °C` a `26.0 °C`.
* **And:** las lecturas son inyectadas exitosamente al sistema como si vinieran de sensores físicos.

### Scenario: Inyección programada de anomalía sintética

* **Given:** el simulador operando en ciclo continuo.
* **When:** se activa el trigger de estrés de prueba `inject_anomaly=True`.
* **Then:** el simulador fuerza la generación de un valor gaussiano atípico superior a `35.0 °C`.
* **And:** el sistema reacciona activando toda la cadena de alertas en menos de `100 ms`.

---

## US-10: Consulta auditable de historial por rango de tiempo

**Etiqueta:** `MoSCoW: Should`
**Story Points:** `3`

> Como administradora de bodega, quiero filtrar y descargar el historial de mediciones de un sensor especificando una fecha y hora de inicio y fin, para analizar tendencias o demostrar el cumplimiento ambiental ante auditores de calidad.

### Scenario: Búsqueda de lecturas en rango válido

* **Given:** un sensor `TEMP_01` con 1000 lecturas almacenadas en la base de datos.
* **When:** consulto el historial para el intervalo entre `2026-07-21 08:00:00` y `2026-07-21 12:00:00`.
* **Then:** el sistema retorna un listado cronológico con únicamente las lecturas registradas en esa ventana.
* **And:** el listado incluye el valor, la unidad y el estado de cada medición.

### Scenario: Consulta en rango sin lecturas

* **Given:** una consulta al historial para una ventana de tiempo futura o sin actividad.
* **When:** se ejecuta la búsqueda.
* **Then:** el sistema retorna una lista vacía `[]`.
* **And:** responde con un mensaje informativo de `No hay registros en el periodo seleccionado`.

---

## US-11: Alerta combinada de alta criticidad (Degradación térmica y humedad)

**Etiqueta:** `MoSCoW: Could`
**Story Points:** `5`

> Como administradora de bodega, quiero que el sistema active una alarma de criticidad máxima si un sector de la bodega supera el umbral de temperatura y el de humedad simultáneamente, para identificar condiciones extremas que estropearán el inventario de forma inminente.

### Scenario: Activación de alerta crítica combinada

* **Given:** un sensor de temperatura `TEMP_01` registrando `36.5 °C`.
* **And:** un sensor de humedad `HUM_01` en el mismo sector registrando `85.0 %` dentro de la misma ventana de 30 segundos.
* **When:** ambas lecturas son procesadas por el motor de reglas.
* **Then:** el sistema emite una alarma de grado `CRITICAL_ENVIRONMENTAL_HAZARD`.
* **And:** activa simultáneamente las alertas en consola y en el archivo de bitácora con prioridad alta.

---

## US-12: Contenerización de la API con Docker

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `3`

> Como desarrolladora backend, quiero empaquetar mi aplicación FastAPI en una imagen de Docker, para garantizar que el código se ejecute en un entorno idéntico independientemente de la máquina host.

### Scenario: Construcción exitosa de la imagen optimizada

* **Given:** un `Dockerfile` configurado con una imagen base ligera.
* **When:** ejecuto el comando `docker build`.
* **Then:** el sistema genera una imagen de contenedor almacenando las dependencias en caché.
* **And:** la imagen final contiene únicamente el código y las dependencias necesarias.

### Scenario: Ejecución del contenedor en el puerto local

* **Given:** la imagen de Docker construida correctamente.
* **When:** levanto el contenedor mapeando el puerto `8000`.
* **Then:** la API responde exitosamente a las peticiones HTTP en `localhost:8000`.
* **And:** los logs de Uvicorn se reflejan en la salida estándar del contenedor.

---

## US-13: Orquestación local con Docker Compose y PostgreSQL

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `5`

> Como ingeniera DevOps, quiero utilizar Docker Compose para levantar la API y una base de datos PostgreSQL simultáneamente, para simular el entorno de producción localmente con un solo comando sin instalaciones manuales.

### Scenario: Levantamiento simultáneo de servicios

* **Given:** un archivo `docker-compose.yml` con los servicios `api` y `db`.
* **When:** ejecuto el comando `docker compose up`.
* **Then:** el motor de Docker descarga la imagen oficial de PostgreSQL.
* **And:** levanta la base de datos inyectando las credenciales por variables de entorno.
* **And:** levanta la API garantizando que la red interna entre ambos funcione.

### Scenario: Conexión de la API a la base de datos orquestada

* **Given:** ambos contenedores en ejecución dentro de la red de Compose.
* **When:** la API intenta inicializar la conexión usando la `DATABASE_URL`.
* **Then:** el host se resuelve correctamente mediante el nombre del servicio (`db`).
* **And:** las tablas de SQLAlchemy se crean exitosamente en PostgreSQL.

---

## US-14: Pipeline de Integración Continua (CI) con GitHub Actions

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `5`

> Como líder técnica, quiero que GitHub Actions ejecute un pipeline de validación en cada push, para asegurar que el código nuevo no rompa las pruebas existentes ni degrade la calidad del tipado y estilo.

### Scenario: Ejecución de pipeline en verde

* **Given:** un archivo de workflow `.github/workflows/ci.yml`.
* **When:** realizo un push a cualquier rama.
* **Then:** el runner de GitHub instala las dependencias y ejecuta Ruff, Mypy y Pytest.
* **And:** todas las herramientas pasan exitosamente manteniendo una cobertura `>= 80%`.
* **And:** el badge del README se actualiza a estado `passing`.

### Scenario: Intercepción de código defectuoso

* **Given:** un commit que contiene un error de sintaxis o rompe un test.
* **When:** realizo un push al repositorio.
* **Then:** el runner de GitHub detecta el fallo durante la ejecución de Pytest.
* **And:** el pipeline se marca como fallido (rojo), bloqueando simbólicamente la integración.

---

## US-15: Despliegue Continuo (CD) a Producción en Render

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `5`

> Como stakeholder, quiero que la aplicación viva esté accesible en internet y se actualice automáticamente al modificar la rama principal, para poder consumir los endpoints reales y validar la documentación Swagger desde cualquier lugar.

### Scenario: Despliegue inicial a producción

* **Given:** el repositorio conectado a un Web Service en Render.com.
* **And:** las variables de entorno de producción configuradas en el dashboard (sin secretos en código).
* **When:** Render detecta la conexión y el Dockerfile.
* **Then:** construye la imagen en la nube y despliega el servicio.
* **And:** la ruta pública `/docs` responde con la interfaz de Swagger.

### Scenario: Actualización automática por Continuous Deployment

* **Given:** el servicio operando normalmente en Render.
* **When:** realizo un merge o push directamente a la rama `main`.
* **Then:** Render intercepta el webhook de GitHub automáticamente.
* **And:** redespliega la nueva versión sin requerir intervención manual.

---

## US-16: Endurecimiento del Pipeline y Seguridad (Extensión Alto Potencial)

**Etiqueta:** `MoSCoW: Could`
**Story Points:** `8`

> Como ingeniera SRE, quiero integrar pruebas de seguridad y tests más rigurosos, para certificar que nuestro artefacto está listo para grado empresarial.

### Scenario: Reducción del tamaño de la imagen

* **Given:** un `Dockerfile` refactorizado usando el patrón Multi-stage build.
* **When:** construyo la imagen para producción.
* **Then:** el peso final del artefacto es inferior a `200 MB`.
* **And:** no incluye herramientas exclusivas de desarrollo (como compiladores de C).

### Scenario: Escaneo de vulnerabilidades en CI

* **Given:** el workflow de GitHub Actions configurado.
* **When:** el pipeline avanza a la etapa de seguridad.
* **Then:** la herramienta Trivy escanea la imagen Docker construida.
* **And:** si encuentra vulnerabilidades críticas, alerta al equipo en los logs del pipeline.


---

# User Stories - Semana 6 + Expansión

## US-01: Gestión de inventario de sensores (CRUD y Soft Delete)

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `3`

> Como administrador del sistema, quiero registrar, consultar, actualizar y desactivar sensores en la base de datos, para mantener un inventario exacto sin perder el historial de lecturas antiguas.

### Scenario: Registro de un nuevo sensor con datos válidos

* **Given:** un payload con ubicación, tipo (`TEMPERATURE`) y umbral de alerta válido.
* **When:** el cliente envía una petición `POST` a `/sensors`.
* **Then:** el sistema guarda el sensor en PostgreSQL.
* **And:** responde con código HTTP `201` y el ID generado.

### Scenario: Desactivación segura de un sensor (Soft Delete)

* **Given:** el sensor con ID `5` que existe y está activo (`is_active=true`).
* **When:** el administrador envía una petición `DELETE` a `/sensors/5`.
* **Then:** el sistema no borra el registro de la base de datos.
* **And:** actualiza el campo `is_active` a `false`, devolviendo código HTTP `204`.

### Scenario: Consulta omitiendo sensores inactivos

* **Given:** que existen sensores activos e inactivos en la base de datos.
* **When:** el usuario hace un `GET` a `/sensors`.
* **Then:** el sistema retorna únicamente la lista de sensores donde `is_active=true`.

---

## US-02: Ingesta de telemetría con validación física

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `5`

> Como dispositivo IoT, quiero enviar mis lecturas a la API mediante un endpoint REST, para que el sistema registre mis mediciones asegurando que los valores son físicamente posibles.

### Scenario: Recepción exitosa de lectura válida

* **Given:** un sensor de tipo `TEMPERATURE` activo en el sistema con ID `10`.
* **When:** el sensor envía un `POST` a `/readings` con valor `25.5` y unidad `C`.
* **Then:** el sistema almacena la lectura asociada al sensor.
* **And:** retorna un HTTP `201` con los detalles de la lectura.

### Scenario: Rechazo por valor físicamente imposible

* **Given:** un sensor de humedad (`HUMIDITY`) con límites de `0` a `100%`.
* **When:** se envía un `POST` a `/readings` con valor `150.0` y unidad `%`.
* **Then:** el sistema rechaza la lectura por violar el límite superior.
* **And:** responde con HTTP `422` (*Unprocessable Entity*) o `400`, explicando el error.

---

## US-03: Detección automática de anomalías en tiempo real

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `5`

> Como operador de planta, quiero que el sistema evalúe cada lectura en el momento de la ingesta, para generar una alerta inmediata si el valor supera el umbral configurado del sensor.

### Scenario: Lectura excede el umbral y genera alerta

* **Given:** un sensor con un `alert_threshold` de `40.0 °C`.
* **When:** ingresa una nueva lectura con un valor de `42.5 °C`.
* **Then:** la lectura se guarda exitosamente.
* **And:** el sistema crea automáticamente un registro en la tabla de Alertas con estado `OPEN`.

### Scenario: Lectura normal no genera alerta

* **Given:** un sensor con un `alert_threshold` de `40.0 °C`.
* **When:** ingresa una nueva lectura con un valor de `39.9 °C`.
* **Then:** la lectura se guarda exitosamente.
* **And:** no se genera ningún registro nuevo en la tabla de Alertas.

---

## US-04: Gestión del ciclo de vida de las alertas

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `3`

> Como técnico de mantenimiento, quiero consultar las alertas activas y cambiar su estado de resolución, para coordinar la atención a las fallas de los equipos en la planta.

### Scenario: Transición de estado válida

* **Given:** una alerta existente en estado `OPEN`.
* **When:** el técnico envía un `PATCH` a `/alerts/{id}` con el nuevo estado `ACKNOWLEDGED`.
* **Then:** el sistema actualiza el estado de la alerta.
* **And:** retorna el registro actualizado con código HTTP `200`.

### Scenario: Bloqueo de transición de estado inválida

* **Given:** una alerta que ya se encuentra en estado `RESOLVED`.
* **When:** el técnico intenta cambiar su estado regresándolo a `OPEN`.
* **Then:** el sistema rechaza la operación por transición de estado prohibida.
* **And:** retorna un error HTTP `400` (*Bad Request*).

---

## US-05: Consulta avanzada de lecturas (Paginación y Filtros)

**Etiqueta:** `MoSCoW: Should`
**Story Points:** `3`

> Como analista de datos, quiero buscar el historial de lecturas de un sensor filtrando por fechas y usando paginación, para no sobrecargar el servidor al pedir miles de registros simultáneamente.

### Scenario: Consulta con filtro de fechas

* **Given:** un sensor con lecturas registradas durante todo el mes.
* **When:** el cliente envía un `GET` a `/readings/{sensor_id}?start_date=2026-08-01&end_date=2026-08-02`.
* **Then:** el sistema devuelve solo los registros de esos dos días.

### Scenario: Límite de paginación aplicado

* **Given:** un sensor con `500` lecturas en la base de datos.
* **When:** el cliente solicita las lecturas con parámetro `limit=50`.
* **Then:** el sistema devuelve exactamente `50` registros.
* **And:** provee información para solicitar la siguiente página (`offset`).

---

## US-06: Motor de estadísticas por sensor

**Etiqueta:** `MoSCoW: Should`
**Story Points:** `3`

> Como gerente de operaciones, quiero consultar el mínimo, máximo y promedio de un sensor en un rango de fechas, para obtener un resumen ejecutivo del comportamiento ambiental sin procesar datos crudos.

### Scenario: Cálculo de estadísticas en periodo con datos

* **Given:** un sensor con lecturas válidas en la última semana.
* **When:** se solicita un `GET` a `/sensors/{id}/stats` para dicho periodo.
* **Then:** el sistema procesa los datos mediante SQL.
* **And:** retorna un objeto JSON con las llaves `min`, `max` y `avg` correctamente calculadas.

---

## US-07: Telemetría del Sistema (Healthcheck)

**Etiqueta:** `MoSCoW: Must`
**Story Points:** `1`

> Como orquestador de nube, quiero consultar un endpoint rápido y ligero de salud, para saber si debo reiniciar el contenedor de la aplicación.

### Scenario: Sistema operando correctamente

* **Given:** que la API está corriendo y PostgreSQL acepta conexiones.
* **When:** se realiza un `GET` a `/health`.
* **Then:** el sistema devuelve HTTP `200` con el payload:

```json
{
  "status": "ok",
  "db": "connected"
}
```

---

## US-08 (Track A): Worker Bridge MQTT a REST

**Etiqueta:** `MoSCoW: Could`
**Story Points:** `8`

> Como arquitecto IoT, quiero un worker en Python independiente que escuche mensajes en un broker MQTT y los envíe a la API REST, para permitir que los microcontroladores de bajo consumo envíen telemetría sin usar HTTP pesado.

### Scenario: Ingesta de payload MQTT exitosa

* **Given:** el broker Mosquitto en ejecución y el worker suscrito al tópico `sensorhub/telemetry`.
* **When:** un dispositivo publica un JSON válido en dicho tópico.
* **Then:** el worker parsea el payload y ejecuta un `POST` HTTP hacia `/readings` de la API.
* **And:** registra en sus logs internos el éxito de la transferencia.

---

# Tareas Técnicas

## TC-01: Infraestructura Base (Docker Compose + BD)

**Etiqueta:** `Tech Chore`
**Story Points:** `3`

> Como DevOps del equipo, quiero configurar `docker-compose.yml` para PostgreSQL y preparar el entorno de migraciones con Alembic, para que todo el desarrollo se realice en un entorno que imite al de producción.

### Scenario: Despliegue local con base de datos limpia

* **Given:** el repositorio clonado sin bases de datos locales.
* **When:** se ejecuta `docker compose up -d`.
* **Then:** el contenedor de PostgreSQL 16 inicia correctamente.
* **And:** se puede ejecutar `alembic upgrade head` para crear las tablas físicas.

---

## TC-02: Pipeline de Integración y Despliegue Continuo (CI/CD)

**Etiqueta:** `Tech Chore`
**Story Points:** `5`

> Como líder de calidad de software, quiero que GitHub Actions corra pruebas estrictas y Render despliegue automáticamente los cambios, para garantizar que no llegue código roto a producción.

### Scenario: Prevención de merge con pruebas fallidas

* **Given:** un Pull Request que contiene un error de lógica de negocio (tests en rojo).
* **When:** GitHub Actions ejecuta el workflow `ci.yml` (`Pytest`, `Ruff`, `Mypy`).
* **Then:** el pipeline falla y se marca con un aspa roja.
* **And:** se bloquea la posibilidad de hacer merge automático a `main`.

---

## TC-03: Centralización de Logs Estructurados

**Etiqueta:** `Tech Chore`
**Story Points:** `2`

> Como ingeniero SRE, quiero que todos los mensajes de consola de la API usen la librería estándar `logging` de Python (preferiblemente en JSON), para tener visibilidad profunda del flujo del sistema en los logs de Render.

### Scenario: Registro de una advertencia por lectura rechazada

* **Given:** el sistema con el logger configurado en nivel `INFO`.
* **When:** un sensor intenta enviar una lectura con formato inválido.
* **Then:** en lugar de usar `print()`, el sistema emite un log de nivel `WARNING`.
* **And:** el log contiene detalles estructurados (ej. IP de origen, razón del fallo) sin colgar la petición.

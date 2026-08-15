## US-01: Verificar y registrar conexión de sensor nuevo
**Etiqueta:** `MoSCoW: Must` | **Story Points:** `2`
Como administradora de bodega,
quiero que el sistema detecte y registre automáticamente cualquier sensor nuevo que se conecte,
para mantener un inventario actualizado de los dispositivos de monitoreo en la planta.

Scenario: Registro exitoso de sensor nuevo
* Given un sensor con ID "TEMP_01" que no está registrado en el sistema
* When el sensor envía su paquete de inicialización y handshake
* Then el sistema lo registra en el inventario activo con estado "OK"
* And el dispositivo queda disponible para consulta en el historial de conexiones

Scenario: Reconexión de sensor ya existente
* Given un sensor con ID "TEMP_01" que ya existe en el registro del sistema
* When el sensor envía su paquete de inicialización tras un reinicio
* Then el sistema restablece su sesión con estado "OK" sin duplicar el registro
* And se registra el evento de reconexión en el historial

## US-02: Categorización automática por tipo de medición
**Etiqueta:** `MoSCoW: Must` | **Story Points:** `3`
Como administradora de bodega,
quiero que el sistema clasifique los sensores automáticamente según sus unidades de medición desde su primer payload,
para asignarles las reglas de validación y almacenamiento correctas sin tiempos de espera.

Scenario: Categorización de sensor de temperatura
* Given un sensor recién conectado que envía un payload de prueba
* When el payload incluye la unidad de medición en "C", "F" o "K"
* Then el sistema clasifica el sensor en la categoría "TEMPERATURE"
* And le asigna el identificador estándar correspondiente (ej. "TEMP_01")

Scenario: Categorización de sensor de humedad
* Given un sensor recién conectado que envía un payload de prueba
* When el payload incluye la unidad de medición en "%H"
* Then el sistema clasifica el sensor en la categoría "HUMIDITY"
* And le asigna el identificador estándar correspondiente (ej. "HUM_01")

Scenario: Rechazo de sensor con unidades desconocidas
* Given un sensor recién conectado que envía un payload de prueba
* When el payload incluye unidades no soportadas (ej. "LUMENS" o "PSI")
* Then el sistema rechaza la conexión con el estado "UNSUPPORTED_TYPE"
* And elimina el dispositivo del registro temporal

## US-03: Validación estricta de 10 sensores activos
**Etiqueta:** `MoSCoW: Must` | **Story Points:** `5`
Como administradora de bodega,
quiero que el monitoreo solo inicie cuando haya exactamente 10 sensores calibrados y activos,
para garantizar la cobertura térmica y de humedad completa en toda la superficie industrial.

Scenario: Inicio exitoso con exactamente 10 sensores
* Given que existen exactamente 10 sensores registrados y activos en el sistema
* When el sistema inicia el ciclo de monitoreo continuo
* Then el estado general cambia a "MONITORING_ACTIVE"
* And el motor de ingesta comienza a procesar lecturas cada 30 segundos

Scenario: Bloqueo por déficit de sensores (Menos de 10)
* Given que hay 9 o menos sensores activos en el sistema
* When se intenta iniciar el ciclo de monitoreo continuo
* Then el sistema lanza una excepción `InsufficientSensorsException`
* And el monitoreo permanece en estado "STOPPED"
* And se escribe el error de déficit de cobertura en el archivo `problemlog.md`

Scenario: Bloqueo por exceso de sensores (Más de 10)
* Given que hay 11 o más sensores enviando tramas al sistema
* When se intenta iniciar el ciclo de monitoreo continuo
* Then el sistema lanza una excepción `LimitExceededException`
* And el monitoreo permanece en estado "STOPPED"
* And se escribe el error de sobrecapacidad en el archivo `problemlog.md`

## US-04: Control de tasa de muestreo (Rate Limiting de 30s)
**Etiqueta:** `MoSCoW: Must` | **Story Points:** `3`
Como administradora de bodega,
quiero limitar la recepción de datos de cada sensor a una lectura máximo cada 30 segundos,
para evitar la saturación de la base de datos y filtrar ruidos por envíos compulsivos del hardware.

Scenario: Lectura aceptada respetando el intervalo
* Given que el sensor "TEMP_01" realizó su última lectura hace 30 segundos o más
* When envía una nueva lectura válida al sistema
* Then la lectura se procesa y se almacena en el historial con estado "OK"

Scenario: Lectura descartada por frecuencia excesiva (Spamming)
* Given que el sensor "TEMP_01" realizó su última lectura hace 12 segundos
* When envía una nueva lectura al sistema
* Then la lectura es descartada por el limitador de frecuencia
* And se almacena un registro de evento descartado con estado "RATE_LIMIT_EXCEEDED"
* And no se altera el timestamp de la última lectura válida

## US-05: Normalización y conversión de temperaturas a Celsius
**Etiqueta:** `MoSCoW: Should` | **Story Points:** `2`
Como administradora de bodega,
quiero que todas las mediciones térmicas en Fahrenheit o Kelvin se conviertan automáticamente a Celsius antes de procesarse,
para estandarizar las comparaciones con los umbrales de anomalía del negocio.

Scenario: Conversión exitosa desde Fahrenheit
* Given una lectura recibida de "TEMP_02" con un valor de 95.0 y unidad "F"
* When pasa por el módulo de normalización de datos
* Then el valor se transforma exactamente a 35.0 con unidad "C"
* And se almacena en el historial como 35.0 °C

Scenario: Conversión exitosa desde Kelvin
* Given una lectura recibida de "TEMP_03" con un valor de 308.15 y unidad "K"
* When pasa por el módulo de normalización de datos
* Then el valor se transforma exactamente a 35.0 con unidad "C"
* And se almacena en el historial como 35.0 °C

Scenario: Rechazo de valor físicamente imposible en Kelvin (Caso borde TDD)
* Given una lectura recibida de "TEMP_03" con un valor de -5.0 y unidad "K"
* When pasa por el módulo de normalización de datos
* Then el sistema rechaza la medición lanzando un `InvalidPhysicalValueException`
* And la lectura se registra con estado "ERR_OUT_OF_BOUNDS"

## US-06: Validación de integridad del payload de lectura
**Etiqueta:** `MoSCoW: Must` | **Story Points:** `3`
Como administradora de bodega,
quiero verificar que los paquetes de datos recibidos contengan formatos numéricos válidos y estén dentro del rango físico del sensor,
para prevenir caídas del sistema por datos corruptos o cortocircuitos.

Scenario: Payload íntegro y dentro de rango
* Given el sensor "HUM_01" envía una lectura de 45.5% con timestamp UTC válido
* When el sistema valida la estructura del mensaje
* Then la lectura se marca con estado "OK" y se pasa al detector de anomalías

Scenario: Payload con datos corruptos (No numérico)
* Given un sensor envía una trama donde el valor de lectura es la cadena "ERROR_READ"
* When el sistema intenta parsear el valor flotante
* Then se captura un error de conversión y la lectura se marca como "ERR_CORRUPT_PAYLOAD"
* And el evento se registra en la bitácora de problemas

Scenario: Lectura fuera de rango físico del sensor (Hardware Fault)
* Given el sensor "TEMP_01" envía una lectura de 450.0 °C
* When el sistema compara el valor con los límites de operación del hardware (-50 a 100 °C)
* Then la lectura se descarta por fallo de sensor y se marca como "ERR_HARDWARE_FAULT"

## US-07: Detección de anomalías térmicas y de humedad con alerta en consola
**Etiqueta:** `MoSCoW: Must` | **Story Points:** `5`
Como administradora de bodega,
quiero que el sistema evalúe cada lectura normalizada contra los umbrales de seguridad y emita una alerta visual en consola al superarlos,
para que los operadores reaccionen de inmediato ante riesgos en la mercancía.

Scenario: Umbral de temperatura superado (Anomalía detectada)
* Given un sensor "TEMP_01" que registra una lectura normalizada de 35.1 °C
* And un detector configurado con el umbral límite inyectado de 35.0 °C
* When la lectura es evaluada por el `AnomalyDetector`
* Then se genera un evento de anomalía con severidad "WARNING"
* And el `AlertManager` imprime el mensaje "ALERTA: TEMP_THRESHOLD_BREACHED en TEMP_01 [35.1 °C]" en la consola

Scenario: Umbral de humedad superado (Anomalía detectada)
* Given un sensor "HUM_01" que registra una lectura de 80.5 %
* And un detector configurado con el umbral límite inyectado de 80.0 %
* When la lectura es evaluada por el `AnomalyDetector`
* Then se genera un evento de anomalía con severidad "WARNING"
* And el `AlertManager` imprime el mensaje "ALERTA: HUM_THRESHOLD_BREACHED en HUM_01 [80.5 %]" en la consola

Scenario: Valor en el límite exacto no genera alerta (Caso borde TDD estricto)
* Given un sensor "TEMP_01" que registra una lectura normalizada de exactamente 35.0 °C
* When la lectura es evaluada por el `AnomalyDetector`
* Then no se genera ninguna anomalía
* And el sistema clasifica la medición con estado "NORMAL"

## US-08: Estrategia de persistencia de alertas en archivo de bitácora
**Etiqueta:** `MoSCoW: Must` | **Story Points:** `3`
Como administradora de bodega,
quiero que todas las alertas de anomalías también se escriban en un archivo persistente del sistema,
para mantener un historial de incidentes auditable a largo plazo sin depender de la consola.

Scenario: Escritura de alerta en archivo log
* Given el `AlertManager` tiene configurada la estrategia de salida `FileAlertStrategy` apuntando a `alerts.log`
* When se activa una alerta de tipo "TEMP_THRESHOLD_BREACHED" para el sensor "TEMP_01"
* Then el sistema añade una nueva línea al archivo `alerts.log` con el timestamp exacto, 
  ID del sensor y valormedido
* And el archivo conserva las alertas anteriores sin sobrescribirlas (modo append)

Scenario: Fallo de escritura en disco sin detener la aplicación
* Given que el archivo `alerts.log` está bloqueado o sin permisos de escritura
* When el `AlertManager` intenta escribir una nueva alerta en el disco
* Then se captura una excepción de E/S (`IOException`)
* And el sistema redirige la alerta a la salida de emergencia en consola sin interrumpir el monitoreo

## US-09: Simulación de lecturas con distribución gaussiana (Extensión Alto Potencial)
**Etiqueta:** `MoSCoW: Could` | **Story Points:** `8`
Como administradora de bodega,
quiero disponer de un simulador de sensores que genere datos sintéticos usando una distribución normal (gaussiana),
para probar el rendimiento del sistema de monitoreo y las alertas bajo condiciones de operación realistas sin hardware conectado.

Scenario: Generación de lecturas en rango normal
* Given un `SensorSimulator` configurado con media de 22.0 °C y desviación estándar de 2.0 °C
* When se ejecutan 60 ciclos de simulación
* Then el 95% de las lecturas generadas se mantienen dentro del rango de 18.0 °C a 26.0 °C
* And las lecturas son inyectadas exitosamente al sistema como si vinieran de sensores físicos

Scenario: Inyección programada de anomalía sintética
* Given el simulador operando en ciclo continuo
* When se activa el trigger de estrés de prueba `inject_anomaly=True`
* Then el simulador fuerza la generación de un valor gaussiano atípico superior a 35.0 °C
* And el sistema reacciona activando toda la cadena de alertas en menos de 100 ms

## US-10: Consulta auditable de historial por rango de tiempo
**Etiqueta:** `MoSCoW: Should` | **Story Points:** `3`
Como administradora de bodega,
quiero filtrar y descargar el historial de mediciones de un sensor especificando una fecha y hora de inicio y fin,
para analizar tendencias o demostrar el cumplimiento ambiental ante auditores de calidad.

Scenario: Búsqueda de lecturas en rango válido
* Given un sensor "TEMP_01" con 1000 lecturas almacenadas en la base de datos
* When consulto el historial para el intervalo entre "2026-07-21 08:00:00" y "2026-07-21 12:00:00"
* Then el sistema retorna un listado cronológico con únicamente las lecturas registradas en esa ventana
* And el listado incluye el valor, la unidad y el estado de cada medición

Scenario: Consulta en rango sin lecturas
* Given una consulta al historial para una ventana de tiempo futura o sin actividad
* When se ejecuta la búsqueda
* Then el sistema retorna una lista vacía `[]`
* And responde con un mensaje informativo de "No hay registros en el periodo seleccionado"

## US-11: Alerta combinada de alta criticidad (Degradación térmica y humedad)
**Etiqueta:** `MoSCoW: Could` | **Story Points:** `5`
Como administradora de bodega,
quiero que el sistema active una alarma de criticidad máxima si un sector de la bodega supera el umbral de temperatura y el de humedad simultáneamente,
para identificar condiciones extremas que estropearán el inventario de forma inminente.

Scenario: Activación de alerta crítica combinada
* Given un sensor de temperatura "TEMP_01" registrando 36.5 °C
* And un sensor de humedad "HUM_01" en el mismo sector registrando 85.0 % dentro de la misma ventana de 30 segundos
* When ambas lecturas son procesadas por el motor de reglas
* Then el sistema emite una alarma de grado "CRITICAL_ENVIRONMENTAL_HAZARD"
* And activa simultáneamente las alertas en consola y en el archivo de bitácora con prioridad alta
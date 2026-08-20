#!/bin/bash

echo "🚀 Iniciando el Workflow de creación de User Stories para SensorHub..."

# 1. Crear las etiquetas (labels) personalizadas para evitar errores
echo "Generando etiquetas..."
gh label create "MoSCoW: Must" --color "E99695" --force 2>/dev/null
gh label create "MoSCoW: Should" --color "F9D0C4" --force 2>/dev/null
gh label create "MoSCoW: Could" --color "FEF2C0" --force 2>/dev/null
gh label create "Tech Chore" --color "C5DEF5" --force 2>/dev/null

# 2. Creación de Issues vía Heredoc (pasa el Markdown directamente por la terminal)

echo "Creando US-01..."
cat << 'EOF' | gh issue create --title "US-01: Gestión de inventario de sensores (CRUD y Soft Delete)" --label "MoSCoW: Must" -F -
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
EOF

echo "Creando US-02..."
cat << 'EOF' | gh issue create --title "US-02: Ingesta de telemetría con validación física" --label "MoSCoW: Must" -F -
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
EOF

echo "Creando US-03..."
cat << 'EOF' | gh issue create --title "US-03: Detección automática de anomalías en tiempo real" --label "MoSCoW: Must" -F -
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
EOF

echo "Creando US-04..."
cat << 'EOF' | gh issue create --title "US-04: Gestión del ciclo de vida de las alertas" --label "MoSCoW: Must" -F -
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
EOF

echo "Creando US-05..."
cat << 'EOF' | gh issue create --title "US-05: Consulta avanzada de lecturas (Paginación y Filtros)" --label "MoSCoW: Should" -F -
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
EOF

echo "Creando US-06..."
cat << 'EOF' | gh issue create --title "US-06: Motor de estadísticas por sensor" --label "MoSCoW: Should" -F -
**Story Points:** `3`

> Como gerente de operaciones, quiero consultar el mínimo, máximo y promedio de un sensor en un rango de fechas, para obtener un resumen ejecutivo del comportamiento ambiental sin procesar datos crudos.

### Scenario: Cálculo de estadísticas en periodo con datos
* **Given:** un sensor con lecturas válidas en la última semana.
* **When:** se solicita un `GET` a `/sensors/{id}/stats` para dicho periodo.
* **Then:** el sistema procesa los datos mediante SQL.
* **And:** retorna un objeto JSON con las llaves `min`, `max` y `avg` correctamente calculadas.
EOF

echo "Creando US-07..."
cat << 'EOF' | gh issue create --title "US-07: Telemetría del Sistema (Healthcheck)" --label "MoSCoW: Must" -F -
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
EOF

echo "Creando US-08..."
cat << 'EOF' | gh issue create --title "US-08 (Track A): Worker Bridge MQTT a REST" --label "MoSCoW: Could" -F -
**Story Points:** `8`

> Como arquitecto IoT, quiero un worker en Python independiente que escuche mensajes en un broker MQTT y los envíe a la API REST, para permitir que los microcontroladores de bajo consumo envíen telemetría sin usar HTTP pesado.

### Scenario: Ingesta de payload MQTT exitosa
* **Given:** el broker Mosquitto en ejecución y el worker suscrito al tópico `sensorhub/telemetry`.
* **When:** un dispositivo publica un JSON válido en dicho tópico.
* **Then:** el worker parsea el payload y ejecuta un `POST` HTTP hacia `/readings` de la API.
* **And:** registra en sus logs internos el éxito de la transferencia.
EOF

echo "Creando TC-01..."
cat << 'EOF' | gh issue create --title "TC-01: Infraestructura Base (Docker Compose + BD)" --label "Tech Chore" -F -
**Story Points:** `3`

> Como DevOps del equipo, quiero configurar `docker-compose.yml` para PostgreSQL y preparar el entorno de migraciones con Alembic, para que todo el desarrollo se realice en un entorno que imite al de producción.

### Scenario: Despliegue local con base de datos limpia
* **Given:** el repositorio clonado sin bases de datos locales.
* **When:** se ejecuta `docker compose up -d`.
* **Then:** el contenedor de PostgreSQL 16 inicia correctamente.
* **And:** se puede ejecutar `alembic upgrade head` para crear las tablas físicas.
EOF

echo "Creando TC-02..."
cat << 'EOF' | gh issue create --title "TC-02: Pipeline de Integración y Despliegue Continuo (CI/CD)" --label "Tech Chore" -F -
**Story Points:** `5`

> Como líder de calidad de software, quiero que GitHub Actions corra pruebas estrictas y Render despliegue automáticamente los cambios, para garantizar que no llegue código roto a producción.

### Scenario: Prevención de merge con pruebas fallidas
* **Given:** un Pull Request que contiene un error de lógica de negocio (tests en rojo).
* **When:** GitHub Actions ejecuta el workflow `ci.yml` (`Pytest`, `Ruff`, `Mypy`).
* **Then:** el pipeline falla y se marca con un aspa roja.
* **And:** se bloquea la posibilidad de hacer merge automático a `main`.
EOF

echo "Creando TC-03..."
cat << 'EOF' | gh issue create --title "TC-03: Centralización de Logs Estructurados" --label "Tech Chore" -F -
**Story Points:** `2`

> Como ingeniero SRE, quiero que todos los mensajes de consola de la API usen la librería estándar `logging` de Python (preferiblemente en JSON), para tener visibilidad profunda del flujo del sistema en los logs de Render.

### Scenario: Registro de una advertencia por lectura rechazada
* **Given:** el sistema con el logger configurado en nivel `INFO`.
* **When:** un sensor intenta enviar una lectura con formato inválido.
* **Then:** en lugar de usar `print()`, el sistema emite un log de nivel `WARNING`.
* **And:** el log contiene detalles estructurados (ej. IP de origen, razón del fallo) sin colgar la petición.
EOF

echo "Todas las historias y tareas técnicas han sido creadas exitosamente en tu repositorio"
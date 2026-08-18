# ADR 0002: Uso de PATCH vs PUT para la actualización parcial de Sensores

## Estado
Aceptado

## Contexto
Conforme la API de SensorHub evolucionó para soportar la gestión completa del inventario (CRUD), surgió la necesidad de definir cómo los clientes y dispositivos IoT actualizarían la información de un sensor existente.

El estándar estricto de REST sugiere el uso de `PUT` para actualizaciones, pero este método exige que el cliente envíe la representación **completa** del recurso. En un entorno de hardware e IoT, obligar a un microcontrolador a descargar todo el estado del sensor (`GET`), modificar un solo parámetro en memoria (ej. el `alert_threshold`), y volver a enviar el objeto completo (`PUT`) resulta ineficiente. Esto aumenta drásticamente el consumo de red, memoria y batería del dispositivo. Además, incrementa el riesgo de condiciones de carrera si dos clientes intentan modificar atributos distintos simultáneamente.

## Decisión
Decidimos utilizar el método HTTP `PATCH` (`PATCH /sensors/{id}`) para permitir actualizaciones parciales, en lugar de forzar el uso estricto de `PUT`.

Técnicamente, esto se implementó en nuestra arquitectura de la siguiente manera:
* **Schemas (Pydantic):** Se creó un esquema dedicado llamado `SensorUpdate` donde todos los campos físicos y de configuración son opcionales (`Optional[...]`).
* **Services/Repositories:** Se instruyó a la lógica de actualización a utilizar el método `model_dump(exclude_unset=True)` al procesar el esquema. Esto asegura que el ORM de SQLAlchemy solo construya una consulta `UPDATE` con las columnas que el cliente explícitamente incluyó en el body de la petición, manteniendo el resto de los datos intactos.

## Consecuencias

### Positivas
* **Eficiencia de Ancho de Banda y Batería:** Los dispositivos IoT solo transmiten los datos estrictamente necesarios (ej. `{"is_active": false}`), lo cual es ideal para redes industriales limitadas o dispositivos de bajo consumo.
* **Prevención de Sobrescrituras Accidentales:** Al no requerir el payload completo, el cliente no tiene que adivinar o cachear el estado previo del sensor, evitando borrar datos vitales por accidente.
* **Desacoplamiento del Cliente:** Un dashboard de administración que solo necesita apagar un sensor no se ve obligado a conocer y validar atributos físicos (como `min_value` o `max_value`) que exigiría un `PUT`.

### Negativas
* **Mantenimiento de Esquemas Boilerplate:** Requiere mantener múltiples modelos en la capa de Pydantic (por ejemplo, `SensorCreate` con campos obligatorios vs `SensorUpdate` con campos opcionales) que deben sincronizarse si el dominio cambia.
* **Lógica de Persistencia Dinámica:** El repositorio requiere una lógica de actualización más compleja; debe extraer los campos enviados e iterar sobre ellos dinámicamente usando `setattr()` sobre el modelo de SQLAlchemy antes de hacer el `session.commit()`.
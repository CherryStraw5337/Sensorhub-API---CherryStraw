# Sprint 1 Planning — Sistema de Monitoreo IoT

**Duración del Sprint:** 1 Semana
**Capacidad del equipo:** 1 Desarrollador (15 Story Points máximos)

## Sprint Goal
Establecer el núcleo inmutable de monitoreo y alertas del sistema IoT con alta fiabilidad, garantizando que los sensores se registren de forma segura sin duplicados, y que las anomalías de temperatura y humedad sean detectadas y notificadas mediante múltiples estrategias (consola y disco) sin hardcodear umbrales.

## Sprint Backlog 

*Nota: Todas las tareas están estimadas en bloques estrictos $\le 4\text{ h}$ para asegurar flujo continuo.*

**1. US-01: Verificar y registrar conexión de sensor nuevo (2 SP)**
* *Tarea 1 (2 h):* Diseñar test unitario para manejo de excepciones en consulta de IDs inexistentes (RED) e implementar `SensorRegistry` (GREEN/REFACTOR).
* *Tarea 2 (1.5 h):* Implementar control de unicidad para evitar duplicación de sensores en reconexiones.

**2. US-05: Normalización y conversión de temperaturas a Celsius (2 SP)**
* *Tarea 1 (2 h):* Crear funciones puras con manejo de límite físico (rechazar valores negativos en Kelvin).

**3. US-07: Detección de anomalías térmicas y de humedad (5 SP)**
* *Tarea 1 (2 h):* Definir *dataclass* inmutable `SensorReading`.
* *Tarea 2 (3 h):* Implementar `AnomalyDetector` usando Inyección de Dependencias para los umbrales.
* *Tarea 3 (2 h):* Añadir pruebas de frontera matemática estricta (ej. exactamente 35.0 °C).

**4. US-08: Estrategia de persistencia de alertas en archivo (3 SP)**
* *Tarea 1 (3 h):* Definir `AlertStrategy` usando `Protocol` e implementar `ConsoleAlertStrategy` y `FileAlertStrategy`.
* *Tarea 2 (2 h):* Crear `AlertManager` y aislar tests de escritura en disco usando la fixture `tmp_path` de pytest.

**5. US-10: Consulta auditable de historial por rango de tiempo (3 SP)**
* *Tarea 1 (3 h):* Implementar filtro por timestamps respetando inmutabilidad.

## Definition of Done (DoD)
Para este Sprint, nos adherimos estrictamente a la [DoD general del proyecto](DEFINITION_OF_DONE.md):
1. TDD demostrable en el historial de commits.
2. Cobertura $\ge 80\%$ validada en CI (`pyproject.toml`).
3. Tipado estricto limpio (`mypy`).
4. Estilo de código impecable (`ruff`).
# Revisión de Código por IA - Semana 5

**Módulo revisado:** `ReadingService` (`app/services/reading_service.py`)
**Herramienta / IA utilizada:** Gemini (Modo Code Review)

## Hallazgos y Decisiones

### Observación A: Bypass de Validación Física en Actualizaciones (CRÍTICO)
* **El Problema:** El método `record_reading` valida los límites físicos y las unidades del sensor correctamente, pero `update_reading` pasa los datos directamente al repositorio sin validarlos. Esto corrompe la integridad de la base de datos si se envía un payload malicioso en un PATCH/PUT.
* **Decisión:** **ACEPTADA**.
* **Justificación:** La lógica de negocio y las restricciones del mundo físico (unidades de medida, rangos matemáticos) deben aplicarse en todas las mutaciones de estado, no solo en la creación. 

### Observación B: Acoplamiento al Framework (Violación de DIP)
* **El Problema:** El servicio lanza `fastapi.HTTPException`. Esto acopla la capa de negocio al framework web, rompiendo el Principio de Inversión de Dependencias (Clean Architecture). El servicio no podría reusarse en un worker en segundo plano (ej. Celery/MQTT).
* **Decisión:** **ACEPTADA**.
* **Justificación:** La capa de servicios debe lanzar excepciones de dominio puras (ej. `ValueError` o clases personalizadas). Es responsabilidad de los Routers (controladores) capturar esas excepciones y traducirlas a respuestas HTTP.
# Sprint Retrospective — Sprint 1

**Fecha:** Jueves, 23 de Julio de 2026
**Participantes:** Único desarrollador (Transición de Firmware a Software)

### ¿Qué salió bien?
1. **Adopción estricta de TDD:** Logré mantener el ciclo *Red $\rightarrow$ Green $\rightarrow$ Refactor* intacto. El historial de Git cuenta una historia clara de ingeniería, donde la prueba siempre guio el diseño del código.
2. **Calidad y Cobertura:** Cerrar el Sprint con un 99% de cobertura y automatizar la Definition of Done en `pyproject.toml` garantiza que el código no se degradará en futuros Sprints.
3. **Desacoplamiento:** El uso del Patrón Strategy (`AlertManager`) y la Inyección de Dependencias (`AnomalyDetector`) eliminó los "números mágicos" y las condicionales anidadas típicas del desarrollo tradicional de firmware.

### ¿Qué se puede mejorar?
1. **Gestión inicial del entorno:** Al arrancar el primer ciclo de TDD, experimenté un `ModuleNotFoundError` en Pytest porque no había inicializado correctamente la jerarquía de paquetes de Python (archivos `__init__.py`). Esto rompió el flujo momentáneamente.

### Acción concreta de mejora para el próximo Sprint
* **Script de *scaffolding* (Andamiaje):** Antes de iniciar la primera User Story del Sprint 2, crearé un checklist o ejecutaré un breve script de consola que genere la estructura de carpetas vacías y los archivos `__init__.py` necesarios, garantizando que el entorno esté aislado y listo para que Pytest corra sin falsos negativos de importación.
# Definition of Done (DoD) — Sistema de Monitoreo IoT

Para que un ítem del Product Backlog (User Story) se considere oficialmente **Terminado (Done)** y el incremento pueda ser integrado a producción, debe cumplir obligatoriamente con el siguiente estándar de calidad:

1. **Pruebas Automatizadas y TDD:** Todos los criterios de aceptación (Gherkin: Given/When/Then) han sido traducidos a tests unitarios o de integración comprobables. El historial de Git demuestra la disciplina TDD (Red -> Green -> Refactor).
2. **Cobertura de Código (Coverage):** Las pruebas automatizadas cubren al menos el **80%** de las líneas de código (`--cov-fail-under=80`).
3. **Tipado Estricto:** El código supera la auditoría de `mypy` sin errores, garantizando firmas de funciones y métodos inmutables (`disallow_untyped_defs = true`).
4. **Análisis Estático (Linting):** El código está 100% limpio en `ruff`, respetando las convenciones estructurales y de importación (reglas: E, F, I, UP, B).
5. **Auto-revisión y Flujo Git:** El desarrollo se hizo en una rama aislada (`feature/US-XX`) y se integró a `main` a través de un Pull Request (PR) donde el propio desarrollador leyó su *diff* línea por línea antes de hacer el merge.
6. **Documentación:** El código cuenta con *docstrings* claras y fáciles de interpretar.
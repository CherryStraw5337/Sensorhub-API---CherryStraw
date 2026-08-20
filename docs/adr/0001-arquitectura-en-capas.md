# ADR 0001: Arquitectura en capas para SensorHub

## Estado
Aceptado

## Contexto
En las primeras iteraciones (Semana 0 y 1), la lógica de lectura de sensores y las reglas físicas estaban fuertemente acopladas. Al evolucionar hacia una API REST con FastAPI (Semana 3), vincular directamente los endpoints (routers) con la base de datos (SQLAlchemy) generaba un diseño rígido. 
Necesitábamos poder:
1. Probar la lógica de validación física (ej. límites de temperatura) sin depender de infraestructura externa (base de datos real).
2. Tener flexibilidad para migrar de una base de datos local (SQLite) a una en la nube (PostgreSQL) sin alterar las reglas de negocio.

## Decisión
Implementamos una arquitectura en 4 capas estrictas:
`routers -> services -> repositories -> models`

Aplicamos el Principio de Inversión de Dependencias (DIP - la "D" de SOLID) en la capa de acceso a datos. Los servicios de negocio no interactúan con implementaciones concretas de SQLAlchemy, sino con abstracciones (`Protocol` en Python) que representan los repositorios.

## Consecuencias

### Positivas
* **Testeabilidad Extrema:** Podemos inyectar *Fake Repositories* (en memoria) para ejecutar los tests de la capa de servicio (donde residen las validaciones físicas) en milisegundos, superando fácilmente el 90% de cobertura.
* **Desacoplamiento de Infraestructura:** El cambio de SQLite a PostgreSQL se realizó únicamente tocando la configuración, dejando la capa de dominio intacta.
* **Modularidad:** Cada capa tiene una Responsabilidad Única (SRP).

### Negativas
* **Mayor Verbosidad:** Añadir un nuevo recurso (ej. un nuevo tipo de actuador) requiere crear archivos y código boilerplate a través de las 4 capas, incluso para operaciones CRUD simples.
* **Curva de Aprendizaje:** Exige disciplina de equipo para no "saltarse" las capas (ej. prohibido hacer consultas directas a la BD desde el router).
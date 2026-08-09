# sdlc-electronica-lyla_alice
[![CI](https://github.com/lylaxtraw/sdlc-electronica-lyla_alice/actions/workflows/ci.yml/badge.svg)](https://github.com/lylaxtraw/sdlc-electronica-lyla_alice/actions/workflows/ci.yml)

## Instalación y Configuración del Entorno

Para configurar el entorno de ejecución profesional y garantizar el aislamiento de las dependencias, siga estos pasos desde el directorio raíz del repositorio:

1.  **Crear el entorno virtual aislado:**
    ```bash
    python3 -m venv .venv
    ```

2.  **Activar el entorno virtual:**
    * En macOS y Linux:
        ```bash
        source .venv/bin/activate
        ```
    * En Windows (Git Bash / WSL):
        ```bash
        source .venv/Scripts/activate
        ```

3.  **Instalar las herramientas de desarrollo y dependencias del ecosistema:**
    ```bash
    pip install pytest pytest-cov ruff mypy fastapi uvicorn sqlalchemy alembic httpx
    ```

## Ejecución de la Suite de Pruebas y Auditoría Estática

La verificación del comportamiento y la calidad del código se ejecuta de manera centralizada desde el **directorio raíz del repositorio** utilizando la santísima trinidad de herramientas de análisis en Python:

### 1. Verificación de Ausencia de Errores (`ruff check` y `mypy`)
Antes de correr las pruebas, se debe verificar que los archivos no cuenten con ningún error dentro de ellos. Para ello, debes escribir los siguientes comandos en tu terminal:

* Para ruff:
    ```bash
    python -m ruff check {carpeta/archivo} --fix  > errores_ruff.txt
    ```
* Para mypy:
    ```bash
    python -m mypy {carpeta/archivo} > errores_mypy.txt
    ```

### 2. Pruebas Unitarias Automatizadas (`pytest`)
Para correr el set completo de pruebas unitarias. Para especificar a dónde quieres correr el comando,
puedes abrir `pyproject.toml` y configurar la ruta:

```bash
python -m pytest > pytest_cov.txt
```

## Ejecución de FastAPI
Para correr cualquier API dentro de este repositorio, se usa el siguiente código (Si salta el error 500, asegúrese de borrar el sensorhub.db que se generó la última vez):

```bash
uvicorn app.main:app --reload
```

## Ejecución con Docker
Para ejecutar cualquier API de este repositorio con Docker, se usa este código:
```bash
# 1. Levantar el sistema completo (API + PostgreSQL)
docker compose up --build

# 2. Aplicar migraciones iniciales (Alembic)
DATABASE_URL="postgresql+psycopg://llave_de_database/sensorhub" alembic upgrade head
```
---

## **Semana 1: UART driver**
Este módulo contiene la reimplementación de un driver UART de estilo embebido (tradicionalmente procedural, acoplado y dependiente de estados globales en C) transformado en una arquitectura modular, orientada a objetos y estrictamente tipada en Python moderno.

El diseño se enfoca en eliminar buffers globales y el acoplamiento de protocolos, facilitando la instanciación múltiple del dispositivo y permitiendo pruebas unitarias en aislamiento total del hardware físico.

## Estructura del Módulo

La arquitectura está completamente segregada bajo los principios SOLID, dividiéndose en los siguientes componentes esenciales:

* **`config.py` (Principio de Responsabilidad Única - SRP):** Contiene la clase `UartConfig` diseñada como una `dataclass` inmutable (`frozen=True`). Se encarga exclusivamente de encapsular y validar en su construcción los parámetros del puerto (baudrate estándar, paridad y bits de parada), lanzando excepciones controladas si los parámetros de hardware son inválidos.
* **`parsers.py` (Principios OCP, LSP e ISP):** Define el contrato abstracto `MessageParser` mediante una clase base (`ABC`). Las implementaciones concretas (`ModbusParser` para tramas binarias RTU y `NMEAParser` para sentencias de texto GPS `$GPGGA`) extienden este contrato mediante polimorfismo, permitiendo que la tubería de análisis inspeccione y procese datos sin modificar la lógica base.
* **`device.py` (Principio de Inversión de Dependencias - DIP):** Implementa la clase `UartDevice`. El dispositivo no instancia internamente sus configuraciones ni hardcodea el protocolo; en su lugar, recibe la abstracción de `UartConfig` y `MessageParser` a través de **Inyección de Dependencias** en el constructor. Incluye un buffer de recepción simulado para pruebas en entornos sin hardware real.
* **`recorder.py` (Principio de Responsabilidad Única - SRP):** Clase `DataRecorder` dedicada únicamente a la persistencia en almacenamiento local de los datos procesados. Guarda la información estructurada utilizando el formato estándar **JSON-lines (`.jsonl`)**, donde cada registro es una línea independiente autodescriptiva.

## Reflexión SOLID: Del Hardware al Software Moderno

La transición de escribir drivers en C embebido clásico a estructurar software modular en Python moderno bajo los principios SOLID representa un cambio radical en la mantenibilidad y evolución del código:

1. **Responsabilidad Única (SRP):** En C es común mezclar la lectura del puerto serial, el parseo de bytes y la impresión en pantalla en una sola función monolítica. Al separar esto en clases especializadas (`UartConfig`, `MessageParser`, `DataRecorder`), podemos modificar el formato de guardado a JSON sin riesgo de romper la comunicación con el hardware.
2. **Abierto/Cerrado (OCP) y Sustitución de Liskov (LSP):** En firmware tradicional, agregar un nuevo protocolo requiere añadir bloques `switch-case` o `if-else` interminables. Con polimorfismo y clases abstractas (`MessageParser`), podemos inyectar un nuevo analizador y el coordinador (`UartDevice`) lo consumirá transparentemente sin modificar su código base.
3. **Inversión de Dependencias (DIP):** El mayor logro en testeabilidad. Al no acoplar el dispositivo a un hardware físico hardcodeado, inyectamos dependencias en el constructor, permitiendo realizar pruebas unitarias en aislamiento total dentro de la memoria RAM, logrando una cobertura del 89% en milisegundos sin requerir una placa o puerto físico conectado.

---

## Semana 2: IoT Monitoring Core (Scrum & TDD)
Este módulo marca la transición de un flujo de trabajo de "superloop" hacia un ciclo de vida de desarrollo de software (SDLC) profesional
Se implementó el núcleo de un sistema de monitoreo para una bodega industrial utilizando Desarrollo Guiado por Pruebas (TDD) estricto y metodologías ágiles.
El diseño garantiza que ninguna línea de código de producción sea escrita sin una especificación técnica previa en forma de prueba unitaria, alcanzando una cobertura del 99%.

### **Estructura del Módulo**
La lógica de negocio se fragmentó en componentes desacoplados siguiendo los requerimientos del "Sprint 0":
* `**backlog.md**` (Ingeniería de Requisitos): Contiene 11 User Stories redactadas bajo el estándar Gherkin (Given/When/Then). Cada historia actúa como el datasheet exacto de una funcionalidad, eliminando ambigüedades mediante criterios de aceptación verificables y priorización MoSCoW.
* `**registry.py**` (Gestión de Inventario): Implementa la clase SensorRegistry. Fue el primer componente desarrollado bajo el ciclo Red-Green-Refactor, asegurando la gestión de sensores únicos y el manejo robusto de excepciones como SensorNotFoundError
* `**detector.py**` (Lógica de Umbrales): Clase AnomalyDetector. Aplica Inyección de Dependencias al recibir los umbrales de temperatura (>35°C) y humedad (>80%) en el constructor. Esto permite modificar las reglas de negocio sin alterar el código fuente
* `**alerts.py**` (Patrón Strategy): Implementa el AlertManager. Utiliza el Patrón Estrategia para alternar de forma transparente entre notificaciones por consola (ConsoleAlert) y persistencia en archivos (FileAlert), cumpliendo con el principio de Inversión de Dependencias.

## Reflexión TDD: De la "Protoboard" al Banco de Pruebas Automatizado

El salto del firmware al software asistido por procesos ágiles redefine la fiabilidad del sistema:
Gherkin como Especificación Técnica: En electrónica, un sensor se define por su rango y tiempo de respuesta; en software, Gherkin traduce esa precisión al comportamiento del sistema (ej. "el sistema debe alertar en exactamente 35.1°C").

* **TDD como Filtro de Calidad:** Escribir el test antes que el código (TDD) frente a escribirlo después (TAD) es la diferencia entre diseñar un circuito con simulación previa o intentar arreglarlo después de que se quemó un componente. El historial de Git (RED → GREEN → REFACTOR) es la evidencia innegociable de este rigor.
* **Inyección de Dependencias para Simulación:** Al inyectar un repositorio en memoria (FakeReadingRepository), podemos validar la lógica de detección de anomalías sin hardware real y sin tocar el disco duro, permitiendo ejecuciones de prueba en milisegundos.

---

## Semana 3: SensorHub API (Arquitectura en Capas & Persistencia)
En esta etapa, el proyecto evoluciona de ejercicios aislados a un producto real y escalable. Se diseñó una Arquitectura en 4 Capas conectada a una base de datos relacional (SQLite) mediante SQLAlchemy 2.0, cumpliendo con las convenciones internacionales de las APIs RESTful.
El sistema integra validación física real, rechazando tramas de datos imposibles antes de que lleguen a la capa de persistencia.

### **Estructura del Producto (app/)**
La arquitectura se segregó para permitir la escalabilidad y el intercambio de componentes de infraestructura (como la base de datos) sin afectar la interfaz de usuario:
* `**routers/**` (Capa de Presentación): Gestiona las peticiones HTTP mediante FastAPI. Implementa endpoints REST profesionales (ej. `POST /sensors/{id}/readings`) con paginación y filtros de fecha.
* `**services/**` (Capa de Negocio): Es el "cerebro" del sistema. Aquí se aplica la Validación Física Real, comparando cada lectura contra los límites configurados en la base de datos para el sensor específico.
* `**repositories/**` (Capa de Acceso a Datos): Encapsula toda la interacción con SQLAlchemy. Aislar las consultas SQL en esta capa permite que el resto del sistema sea agnóstico al motor de base de datos utilizado (SQLite, PostgreSQL, etc.).
* `**models/ y schemas/**` (Definición de Contratos): Los modelos ORM definen la estructura relacional (Sensores 1:N Lecturas) con sintaxis Mapped. Los esquemas de Pydantic actúan como el contrato de comunicación, validando y serializando los datos de entrada y salida.

## Reflexión de Arquitectura: El Software como Sistema de Protección

La implementación de una API profesional con arquitectura limpia refuerza la robustez del "SensorHub":
Pydantic como Protección de Capa Física: Al igual que un circuito de protección contra sobretensión, Pydantic escanea las tramas de datos (JSON) y las rechaza con un error 422 (Unprocessable Entity) si detecta ruido o tipos de datos incorrectos antes de que el microcontrolador gaste ciclos procesándolos.

* **SQLAlchemy como Memoria No Volátil:** Pasamos de usar diccionarios en RAM a una base de datos persistente. El uso de índices y transacciones ACID garantiza que los datos de la bodega industrial sean íntegros y consultables en milisegundos, funcionando como una Lookup Table (LUT) de alto rendimiento.
* **Arquitectura en Capas como DIP a Escala:** La separación total permite que los Routers dependan de abstracciones de los Servicios, y estos de los Repositorios. Esto facilitó alcanzar una cobertura de integración del 89.38% mediante el uso de StaticPool en los tests para simular una persistencia compartida en memoria RAM durante la suite de pruebas.

---

## Semana 4: Infraestructura y Despliegue Continuo

En esta etapa, el proyecto SensorHub ha transicionado de un entorno de desarrollo local a una infraestructura de producción automatizada, escalable y robusta. Se ha implementado el flujo completo de DevOps para garantizar que el software sea reproducible y se entregue de forma continua.

### Acceso al Servicio en Producción
* **API (Swagger UI):** [https://sensorhub-api.onrender.com/docs](https://sensorhub-api.onrender.com/docs)
* **Health Check:** [https://sensorhub-api.onrender.com/health](https://sensorhub-api.onrender.com/health)

### Componentes de la Infraestructura
* **Contenerización (Docker):** Implementación de un `Dockerfile` optimizado mediante el patrón Multi-stage build utilizando la imagen base `python:3.12-slim`. Esto permitió reducir el peso del artefacto final a menos de 200 MB y aumentar la seguridad al eliminar herramientas de compilación en la imagen de ejecución.
* **Orquestación (Docker Compose):** Configuración de un entorno local idéntico al de producción que levanta la API de FastAPI junto con una base de datos PostgreSQL 16 mediante un solo comando, gestionando redes internas y volúmenes persistentes.
* **Integración Continua (CI):** Pipeline automatizado en GitHub Actions que ejecuta en cada push:
    * **Linting:** Con Ruff para asegurar código limpio.
    * **Tipado Estático:** Con Mypy para prevenir errores de tipo.
    * **Pruebas Automatizadas:** Con Pytest, garantizando una cobertura de código ≥ 80%.
* **Despliegue Continuo (CD):** Integración con Render.com mediante Infraestructura como Código (`render.yaml`). El sistema realiza un despliegue automático tras cada merge exitoso en la rama `main`, ejecutando las migraciones de base de datos con Alembic de forma previa al arranque del servicio.

### Instrucciones de Ejecución (Docker local)
Para replicar el entorno de producción en su máquina local:

```bash
# 1. Levantar el sistema completo (API + PostgreSQL)
docker compose up --build

# 2. Aplicar migraciones iniciales (Alembic)
DATABASE_URL="postgresql+psycopg://sensor:secret@localhost:5433/sensorhub" alembic upgrade head
```

## Reflexión: De la "Máquina Local" a Producción
La implementación de este pipeline resuelve el problema crítico de "funciona en mi máquina" al empaquetar el entorno completo. Al inyectar la configuración mediante variables de entorno y automatizar las migraciones en el arranque, hemos creado un artefacto inmutable que puede vivir en cualquier proveedor de nube con total seguridad (cero secretos en el historial de Git).
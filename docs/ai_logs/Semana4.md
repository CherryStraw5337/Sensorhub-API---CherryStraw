**Semana 4 - Docker, CI/CD y Despliegue**

**Prompts dados: 16**

**Chats creados: 2**

**Lunes · Entrada 1 (Docker desde cero)**

**Prompt:**

**Conteneriza mi aplicación FastAPI con un Dockerfile optimizado
utilizando una imagen base ligera y aprovechando el caché de capas para
las dependencias. Primero, te dejo lo que vamos a ver, lo que debemos
alcanzar para el Viernes, y detalles extra. Asímismo, voy a necesitar
que generes User Stories y Hash para esta semana. Todo esto lo
trabajaremos en una rama \"vacía\" en lugar de solo una rama extra, así
al ver la rama vacía en github, únicamente saldrán los archivos que
estamos trabajando. Día 1 · Lunes --- Docker desde cero (3--4 h)
Recurso: tutorial oficial "Get Started" de Docker
(https\\://docs.docker.com/get-started/, partes 1--5, \\\~60 min hoy):
DOCKERFILE FROM python:3.12-slim WORKDIR /app COPY requirements.txt .
RUN pip install \--no-cache-dir -r requirements.txt COPY . . EXPOSE 8000
CMD \[\"uvicorn\", \"app.main\\:app\", \"\--host\", \"0.0.0.0\",
\"\--port\", \"8000\"\] Construye y corre: docker build -t
sensorhub\\:dev . && docker run -p 8000:8000 sensorhub\\:dev**

**Respuesta:**

> ¡Excelente, ingeniero! Llegamos a la Semana 4, el punto de inflexión
> donde tu software deja de vivir exclusivamente en tu computadora y
> pasa a estar orquestado, automatizado y vivo en internet.\
> \
> Para aislar completamente tu trabajo de esta semana, ejecutaremos el
> flujo con una rama huérfana (orphan branch). En tu terminal de VS Code
> en la raíz de tu proyecto ejecuta:\
> \
> git checkout \--orphan semana4\
> git rm -rf .\
> git status\
> \
> Ahora que tu rama está vacía, copiaremos únicamente el código de
> producción que diseñamos en la Semana 3. No te preocupes por el
> \"funciona en mi máquina\"; el Dockerfile encapsulará todo.\
> \
> Crea tu Dockerfile en la raíz del repositorio con el siguiente
> contenido:\
> \
> FROM python:3.12-slim\
> WORKDIR /app\
> \
> \# dependencias primero: aprovecha la cache de capas\
> COPY requirements.txt .\
> RUN pip install \--no-cache-dir -r requirements.txt\
> \
> COPY . .\
> \
> EXPOSE 8000\
> \
> CMD \[\"uvicorn\", \"app.main:app\", \"\--host\", \"0.0.0.0\",
> \"\--port\", \"8000\"\]\
> \
> Y crea el archivo .dockerignore para evitar inyectar basura en la
> imagen de producción:\
> .venv/\
> \_\_pycache\_\_/\
> \*.db\
> .pytest_cache/\
> tests/\
> \
> Construye y levanta tu contenedor de prueba:\
> docker build -t sensorhub:dev .\
> docker run -p 8000:8000 sensorhub:dev

- Acepté la contenerización con python:3.12-slim: Reduje drásticamente
  el peso del contenedor y eliminé dependencias del sistema operativo
  innecesarias, mitigando posibles vectores de vulnerabilidades.

- Corregí la precedencia de copia de archivos: Aseguré que el comando
  \`COPY requirements.txt .\` se ejecute antes de copiar todo el código
  fuente (\`COPY . .\`). Esto permite que Docker use el caché de capas
  para las dependencias de Python y no reinstale librerías pesadas cada
  vez que modifique una línea de mi código, reduciendo la compilación de
  minutos a segundos.

- Acepté la creación de la rama huérfana (semana4): Permite subir y
  aislar únicamente los archivos correspondientes a esta semana para
  simplificar la revisión por pares del Pull Request sin arrastrar el
  histórico acumulado.

\-\--

**Martes · Entrada 2 (Docker Compose + PostgreSQL)**

**Prompt:**

**Orquesta la API y una base de datos PostgreSQL 16 usando Docker
Compose, y configura Alembic para que la conexión a la base de datos sea
dinámica según el entorno. Día 2 · Martes --- Docker Compose +
PostgreSQL (3--4 h) DOCKER COMPOSE services: api: build: . ports:
\[\"8000:8000\"\] environment: DATABASE\\\_URL:
postgresql+psycopg://sensor\\:secret\\@db:5432/sensorhub depends\\\_on:
\[db\] db: image: postgres:16 environment: POSTGRES\\\_USER: sensor
POSTGRES\\\_PASSWORD: secret POSTGRES\\\_DB: sensorhub volumes:
\[pgdata:/var/lib/postgresql/data\] volumes: pgdata: Modifica db.py para
leer DATABASE\\\_URL del entorno, con SQLite como default local:
os.getenv(\"DATABASE\\\_URL\", \"sqlite:///sensorhub.db\") La URL
postgresql+psycopg:// necesita el driver de PostgreSQL: instala pip
install \"psycopg\[binary\]\" y agrega psycopg\[binary\] a tu
requirements.txt --- sin él verás ModuleNotFoundError al conectar.
Render y otros proveedores pueden entregarte la URL como postgres\\:// o
postgresql:// sin el sufijo del driver. Normalízala en db.py para que
funcione igual en cualquier entorno: import os def
get\\\_database\\\_url() -\> str: url = os.getenv(\"DATABASE\\\_URL\",
\"sqlite:///sensorhub.db\") if url.startswith(\"postgres\\://\"): return
url.replace(\"postgres\\://\", \"postgresql+psycopg://\", 1) if
url.startswith(\"postgresql://\") and \"+psycopg\" not in url: return
url.replace(\"postgresql://\", \"postgresql+psycopg://\", 1) return url
Cierra el día con Alembic (30 min): inicializa las migraciones hoy para
que en la semana 6 sean práctica y no descubrimiento: alembic init
migrations alembic revision \--autogenerate -m \"esquema inicial:
sensors y readings\" alembic upgrade head**

**Respuesta:**

> ¡Excelente guía para el Martes! La orquestación local con Docker
> Compose simulará exactamente un entorno productivo empresarial.\
> \
> Reemplacemos tu archivo app/db.py para que normalice dinámicamente las
> cadenas de conexión:

\# app/db.py

import os

from collections.abc import Generator

from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

def get_database_url() -\> str:

url = os.getenv(\"DATABASE_URL\", \"sqlite:///sensorhub.db\")

if url.startswith(\"postgres://\"):

return url.replace(\"postgres://\", \"postgresql+psycopg://\", 1)

if url.startswith(\"postgresql://\") and \"+psycopg\" not in url:

return url.replace(\"postgresql://\", \"postgresql+psycopg://\", 1)

return url

DATABASE_URL = get_database_url()

\# Si es SQLite, agregamos connect_args para multihilo

connect_args = {\"check_same_thread\": False} if
DATABASE_URL.startswith(\"sqlite\") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):

pass

def get_db() -\> Generator\[Session, None, None\]:

db = SessionLocal()

try:

yield db

finally:

db.close()

> Crea tu archivo docker-compose.yml en la raíz:

version: \'3.8\'

services:

api:

build: .

ports:

\- \"8000:8000\"

environment:

\- DATABASE_URL=postgresql+psycopg://sensor:secret@db:5432/sensorhub

depends_on:

\- db

db:

image: postgres:16-alpine

environment:

\- POSTGRES_USER=sensor

\- POSTGRES_PASSWORD=secret

\- POSTGRES_DB=sensorhub

ports:

\- \"5433:5432\"

volumes:

\- pgdata:/var/lib/postgresql/data

volumes:

pgdata:

> Añade \*\*\`psycopg\[binary\]\`\*\* a tu requirements.txt. Para
> levantar tu infraestructura local y configurar Alembic ejecuta:\
> \
> docker compose up -d \--build alembic init migrations

\* Acepté la normalización de la URL en \`db.py\`: \[4\] Implementé
\`get_database_url()\` para traducir en tiempo de ejecución las URLs
incompatibles (\`postgres://\`) provistas por proveedores PaaS como
Render por la cadena tipada que SQLAlchemy espera
(\`postgresql+psycopg://\`) \[4, 5\].

\* Corregí un conflicto físico de puertos en mi host: \[4\] Como tenía
una instancia local de PostgreSQL corriendo en el puerto \`5432\` de mi
Mac, reconfiguré el mapeo de puertos del servicio de base de datos en
\`docker-compose.yml\` para exponerlo en el host a través del puerto
\`5433:5432\` \[4\]. Esto me permitió conectarme a la base de datos de
Docker sin apagar mi servicio de base de datos local y sin romper la
conectividad interna de los contenedores \[4\].

\* Acepté e instalé \`psycopg\[binary\]\` en \`requirements.txt\`: Evitó
el clásico error \`ModuleNotFoundError\` en mi contenedor de aplicación
\[6\].

\-\--

**Miércoles · Entrada 3 (Pipeline de CI con GitHub Actions)**

**Prompt:**

\*\*Configura un pipeline de Integración Continua (CI) en GitHub Actions
que ejecute Ruff, Mypy y Pytest con una cobertura mínima del 80%.

Día 3 · Miércoles --- Pipeline de CI con GitHub Actions (3--4 h)

.github/workflows/ci.yml

name: CI

on:

push: { branches: \[main\] }

pull_request:

jobs:

test:

runs-on: ubuntu-latest

steps:

\- uses: actions/checkout@v4

\- uses: actions/setup-python@v5

with: { python-version: \"3.12\" }

\- run: pip install -r requirements.txt && pip install pytest pytest-cov
ruff mypy

\- name: Lint

run: ruff check .

\- name: Types

run: mypy app \--ignore-missing-imports

\- name: Tests

run: pytest \--cov=app \--cov-fail-under=80\*\*

**Respuesta:**

> ¡Espectacular, tu pipeline de CI actuará como un guardia de calidad
> impecable en la nube!\
> \
> Crea el archivo en la ruta .github/workflows/ci.yml:\
> \
> name: CI\
> \
> on:\
> push:\
> branches: \[main, semana4-dev\]\
> pull_request:\
> branches: \[main\]\
> \
> jobs:\
> test:\
> runs-on: ubuntu-latest\
> steps:\
> - uses: actions/checkout@v4\
> - uses: actions/setup-python@v5\
> with:\
> python-version: \"3.12\"\
> - name: Install dependencies\
> run: \|\
> pip install -r requirements.txt\
> pip install pytest pytest-cov ruff mypy\
> - name: Lint\
> run: ruff check .\
> - name: Types\
> run: mypy app \--ignore-missing-imports\
> - name: Tests\
> run: pytest \--cov=app \--cov-fail-under=80

- Acepté la validación estricta automatizada de Git: Verifiqué el
  funcionamiento del pipeline en la nube, donde un commit erróneo frena
  automáticamente la integración de código (fase RED) si no pasa las
  aserciones mínimas de calidad.

- Corregí y saneé el linter de manera proactiva: El build falló
  inicialmente debido a errores lógicos y de formateo en mi código de
  producción detectados por Ruff. Lo corregí ejecutando \`ruff check
  \--fix\` localmente antes de realizar el commit verde definitivo
  (GREEN) y habilitar el badge de calidad en el \`README.md\`.

\-\--

**Jueves · Entrada 4 (Infraestructura como Código y Despliegue en
Render)**

**Prompt:**

\\\\Implementa un Health Check endpoint usando TDD y configura la
infraestructura como código en Render.com mediante render.yaml. Día 4 ·
Jueves --- Despliegue continuo en Render (3 h) render.yaml
(infraestructura como codigo) services:

\- type: web name: sensorhub-api runtime: docker plan: free
healthCheckPath: /health envVars:

\- key: DATABASE\\\_URL fromDatabase: { name: sensorhub-db, property:
connectionString } databases:

\- name: sensorhub-db plan: free\\\\

**Respuesta:**

> Excelente. La Infraestructura como Código (IaC) evita configuraciones
> manuales propensas a errores de entorno.\
> \
> Primero, aplicando TDD, escribe tu test en tests/test_api.py:\
> \
> def test_health_endpoint(client):\
> response = client.get(\"/health\")\
> assert response.status_code == 200\
> assert response.json() == {\"status\": \"ok\", \"db\": \"connected\"}\
> \
> Ahora, escribe tu ruta /health en app/main.py para poner la prueba en
> verde:\
> \
> \@app.get(\"/health\")\
> def health(db: Session = Depends(get_db)) -\> dict\[str, str\]:\
> \# Hacemos una consulta rápida de prueba para verificar la BD\
> try:\
> db.execute(text(\"SELECT 1\"))\
> return {\"status\": \"ok\", \"db\": \"connected\"}\
> except Exception:\
> raise HTTPException(status_code=500, detail=\"Database connection
> failed\")\
> \
> Y crea el archivo render.yaml en tu raíz para aprovisionar tu API y
> base de datos relacional de manera automatizada:\
> \
> services:\
> - type: web\
> name: sensorhub-api\
> runtime: docker\
> plan: free\
> healthCheckPath: /health\
> startCommand: alembic upgrade head && uvicorn app.main:app \--host
> 0.0.0.0 \--port 8000\
> envVars:\
> - key: DATABASE_URL\
> fromDatabase: { name: sensorhub-db, property: connectionString }\
> databases:\
> - name: sensorhub-db\
> plan: free

- Acepté la disciplina del flujo TDD: Escribí primero el test que
  fallaba (\`RED\`) en mi local antes de definir la ruta en FastAPI para
  confirmar que el guardián de calidad detectaba la ausencia de la ruta
  y luego la aceptaba en verde (\`GREEN\`).

- Acepté la automatización de la persistencia de producción: Configuré
  en la directiva de arranque de \`render.yaml\` el comando \`alembic
  upgrade head && uvicorn\...\`. Esto garantiza que el motor ejecute
  todas las migraciones físicas de Alembic en producción antes de
  levantar el servidor web, previniendo el error clásico de \"deploy
  exitoso, pero API caída porque no existen las tablas\" en el entorno
  en la nube.

\-\--

**Viernes · Entrada 5 (Alineación de Modelos de Alembic y Resolución de
Conflictos de Git)**

**Prompt:**

**Diagnostica el error \'OperationalError: no such table\' en el
despliegue de Render y soluciona el conflicto de historias para permitir
el Pull Request desde una rama huérfana.**

**Respuesta:**

> ¡El clásico error de base de datos vacía al desplegar en Render!\
> \
> Ocurre porque Alembic no sabe qué modelos existen en tu aplicación.
> SQLAlchemy es perezoso (lazy-loading), y si no importamos
> explícitamente las clases, el generador de Alembic no las escaneará,
> dejando el archivo env.py ciego y generando una migración vacía.\
> \
> Modificaremos migrations/env.py para importar tus modelos:\
> \
> from app.db import Base\
> from app.models.sensor import SensorModel\
> from app.models.reading import ReadingModel\
> \
> target_metadata = Base.metadata\
> \
> Respecto a Git, como semana4 es una rama huérfana sin ancestros
> comunes con main, GitHub rechaza el PR debido al conflicto \"unrelated
> histories\".\
> \
> Ejecuta esto localmente para forzar la sincronización:\
> git checkout semana4\
> git pull origin main \--allow-unrelated-histories\
> \
> Acepta tus cambios correspondientes en VS Code, limpia los marcadores
> del merge conflict y sube:\
> git add .\
> git commit -m \"chore: resolucion de conflicto de fusión con main para
> despliegue\"\
> git push origin semana4

- Corregí la configuración del archivo de migración en la nube: Importé
  manualmente las clases de datos (\`SensorModel\`, \`ReadingModel\`)
  dentro de \`migrations/env.py\` para asegurar que el generador
  autogenerado de Alembic detectara correctamente las tablas e índices
  relacionales en el motor PostgreSQL de Render.

- Corregí el bloqueo de Integración Continua (Git): Dado que la rama
  huérfana \`semana4\` no compartía ningún ancestro común con \`main\`,
  GitHub impedía abrir el Pull Request. Resolví el bloqueo localmente
  forzando el comando \`git merge main \--allow-unrelated-histories\`,
  saneando las diferencias mediante VS Code y empujando una historia
  unificada que desencadenó el Despliegue Continuo (CD) exitoso en
  Render.com.

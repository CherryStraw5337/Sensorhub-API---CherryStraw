# ==========================================
# ETAPA 1: Builder (La fábrica)
# ==========================================
FROM python:3.12-slim AS builder

# Evitar que Python escriba archivos .pyc y forzar logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Crear el entorno virtual en una ruta estándar
RUN python -m venv /opt/venv
# Asegurar que los comandos pip/python usen este entorno
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build

# Copiamos SOLO el requirements primero. 
# Esto aprovecha la caché de capas de Docker: si no cambias las dependencias, 
# Docker se salta este paso y ahorras mucho tiempo de construcción.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# ETAPA 2: Runner (El producto final)
# ==========================================
FROM python:3.12-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Crear un usuario sin privilegios (appuser) por seguridad
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Inyectamos el entorno virtual ya ensamblado desde la etapa anterior
COPY --from=builder /opt/venv /opt/venv

# Copiamos nuestro código de la API y las migraciones
COPY ./app ./app
COPY alembic.ini .

# Dar propiedad de los archivos al usuario sin privilegios
RUN chown -R appuser:appuser /app

# Cambiar a usuario seguro (todo lo que corra a partir de aquí no será root)
USER appuser

# Documentar el puerto en el que escucha Uvicorn
EXPOSE 8000

# Comando de arranque (nuestro "main" loop)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
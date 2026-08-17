# migrations/env.py

import sys
import os
from logging.config import fileConfig

# MODIFICACIÓN TC-01: No usaremos engine_from_config 
from sqlalchemy import pool # Mantenemos pool para NullPool

from alembic import context

# MODIFICACIÓN ROBUSTA DEL PATH PARA TC-01 (Se mantiene)
# Obtener la ruta absoluta del directorio que contiene este archivo (env.py)
# que es el directorio 'migrations'
migrations_dir = os.path.dirname(os.path.abspath(__file__))
# El directorio raíz del proyecto es el padre de 'migrations'
project_root = os.path.dirname(migrations_dir)
# Añadir el directorio raíz al sys.path
sys.path.append(project_root)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MODIFICACIÓN DE IMPORTACIONES PARA TC-01 (Evitar Circularidad y Usar Engine Centralizado)
# Importamos Base y los modelos individuales de forma explícita.
# NUEVO: Importamos el engine centralizado de app/db.py
from app.db import Base, engine # <-- Solución TC-01
from app.models.sensor import SensorModel

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # MODIFICACIÓN TC-01: Usar la URL del engine importado 
    # Antes: url = config.get_main_option("sqlalchemy.url")
    url = engine.url.render_as_string(hide_password=False)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # MODIFICACIÓN TC-01: Usar el engine importado directamente 
    # Antes: connectable = engine_from_config(...)
    connectable = engine 

    # AJUSTE PARA TC-01: NullPool es recomendado para migraciones online 
    # Reconfiguramos el pool del engine importado para usar NullPool
    # Esto evita conexiones persistentes que podrían bloquear migraciones.
    connectable.pool = pool.NullPool(
        creator=connectable.pool._creator,
        recycle=connectable.pool._recycle,
        echo=connectable.pool._echo
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
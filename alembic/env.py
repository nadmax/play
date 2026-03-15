"""
Alembic environment configuration.

Reads the target database URL from the DATABASE_URL environment variable
and wires the application's SQLAlchemy metadata so that `autogenerate`
can detect schema drift automatically.
"""

import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

from alembic import context
from play.database import Base
from play import models  # noqa: F401


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "The DATABASE_URL environment variable is not set. "
        "Export it before running Alembic, e.g.:\n"
        "  export DATABASE_URL=postgresql://user:pass@localhost:5432/mydb"
    )
config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in *offline* mode (no live DB connection required).

    Alembic emits SQL to stdout / a file instead of executing it directly.
    Useful for generating migration scripts for review or for DBAs to apply.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in *online* mode (requires a live DB connection).

    Creates an engine from the config, connects, and applies pending
    migrations within a transaction.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

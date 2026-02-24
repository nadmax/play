"""
Database configuration module.

This module initializes the SQLAlchemy engine and session factory,
configures SQLite-specific behavior, and provides the declarative base
class for ORM models.

It also exposes a dependency function to provide database sessions.
"""

from sqlalchemy import create_engine, event, orm
from sqlalchemy.engine import Engine
from play import const
import sqlite3

engine = create_engine(const.DATABASE_URL)
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Enable SQLite foreign key enforcement.

    SQLite does not enforce foreign key constraints by default.
    This event listener ensures that the PRAGMA foreign_keys=ON
    setting is applied every time a new connection is created.

    Args:
        dbapi_connection: The raw DB-API connection.
        connection_record: SQLAlchemy connection record (unused).
    """

    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class Base(orm.DeclarativeBase):
    """
    Base class for all ORM models.

    All SQLAlchemy models in the application should inherit from this
    class to share common metadata and configuration.
    """

    pass


def get_db():
    """
    Provide a database session.

    This function is intended to be used as a FastAPI dependency.
    It yields a SQLAlchemy session and ensures it is properly closed
    after the request lifecycle.

    Yields:
        Session: An active SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


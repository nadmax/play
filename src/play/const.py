"""
Application configuration constants.

This module loads required environment variables related to the
PostgreSQL database configuration and builds the SQLAlchemy
database connection URL.

Environment Variables:
    POSTGRES_USER (str): Database username.
    POSTGRES_PASSWORD (str): Database user password.
    POSTGRES_DB (str): Database name.
    POSTGRES_HOST (str): Database host address.
    POSTGRES_PORT (str): Database port.

Raises:
    KeyError: If any required environment variable is missing.
"""

import os

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

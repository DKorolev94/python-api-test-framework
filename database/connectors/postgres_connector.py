import os

import psycopg2
from sshtunnel import SSHTunnelForwarder

from config.settings import settings
from database.exceptions import DatabaseConnectionError
from utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseConnector:
    """PostgreSQL connector with optional SSH tunnel.

    Used only when data cannot be obtained via API.
    """

    def __init__(self):
        self.tunnel = None
        self.connection = None

    def connect(self):
        try:
            if settings.DB_SSH_HOST:
                key_path = os.path.expanduser(settings.DB_SSH_KEY_FILE)
                self.tunnel = SSHTunnelForwarder(
                    (settings.DB_SSH_HOST, settings.DB_SSH_PORT),
                    ssh_username=settings.DB_SSH_USER,
                    ssh_pkey=key_path,
                    remote_bind_address=(settings.DB_HOST, settings.DB_PORT),
                    set_keepalive=30,
                )
                self.tunnel.start()
                logger.info("SSH tunnel started")
                host, port = "127.0.0.1", self.tunnel.local_bind_port
            else:
                host, port = settings.DB_HOST, settings.DB_PORT

            self.connection = psycopg2.connect(
                host=host,
                port=port,
                dbname=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
            )
            logger.info("Database connection established")
            return self.connection
        except Exception as e:
            raise DatabaseConnectionError(f"Connection failed: {e}") from e

    def close(self):
        if self.connection:
            self.connection.close()
        if self.tunnel:
            self.tunnel.stop()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class DatabaseManager:
    """Cursor wrapper with ping-before-execute."""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def execute(self, query: str, params: tuple | None = None) -> None:
        self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

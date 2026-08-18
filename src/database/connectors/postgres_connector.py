from pathlib import Path

import psycopg2

from src.config.settings import settings
from src.database.exceptions import DatabaseConnectionError
from src.utils.logger import get_logger
from src.utils.ssh_tunnel import SSHTunnel

logger = get_logger(__name__)


class DatabaseConnector:
    """Коннектор к PostgreSQL с опциональным SSH-туннелем.

    Используется только когда данные нельзя получить через API.
    """

    def __init__(self):
        self.tunnel = None
        self.connection = None

    def connect(self):
        """Открывает SSH-туннель (если настроен) и соединение с PostgreSQL."""
        try:
            if settings.DB_SSH_HOST:
                key_path = str(Path(settings.DB_SSH_KEY_FILE).expanduser())
                self.tunnel = SSHTunnel(
                    ssh_host=settings.DB_SSH_HOST,
                    ssh_port=settings.DB_SSH_PORT,
                    ssh_user=settings.DB_SSH_USER,
                    ssh_pkey=key_path,
                    remote_binds=[(settings.DB_HOST, settings.DB_PORT)],
                )
                self.tunnel.start()
                host, port = "127.0.0.1", self.tunnel.local_bind_ports[0]
            else:
                host, port = settings.DB_HOST, settings.DB_PORT

            self.connection = psycopg2.connect(
                host=host,
                port=port,
                dbname=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
            )
        except Exception as e:
            message = f"Connection failed: {e}"
            raise DatabaseConnectionError(message) from e
        else:
            logger.info("Database connection established")
            return self.connection

    def close(self):
        """Закрывает соединение с базой и останавливает SSH-туннель, если он был."""
        if self.connection:
            self.connection.close()
        if self.tunnel:
            self.tunnel.stop()

    def __enter__(self):
        """Подключается и возвращает self для использования как контекстный менеджер."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрывает соединение при выходе из контекстного менеджера."""
        self.close()


class DatabaseManager:
    """Обёртка над курсором."""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def execute(self, query: str, params: tuple | None = None) -> None:
        """Выполняет SQL-запрос с необязательными параметрами."""
        self.cursor.execute(query, params)

    def fetchone(self):
        """Возвращает следующую строку последнего выполненного запроса."""
        return self.cursor.fetchone()

    def fetchall(self):
        """Возвращает все оставшиеся строки последнего выполненного запроса."""
        return self.cursor.fetchall()

    def commit(self):
        """Фиксирует текущую транзакцию."""
        self.connection.commit()

    def rollback(self):
        """Откатывает текущую транзакцию."""
        self.connection.rollback()

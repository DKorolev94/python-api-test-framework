from src.database.connectors.postgres_connector import DatabaseManager
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DBOperation:
    """Запросы к БД под конкретные задачи.

    Используются только когда данные нельзя получить через API.
    Каждый метод это одна атомарная операция: коммит при успехе, откат при ошибке.
    В SQL всегда используем плейсхолдеры %s, f-строки не используем.
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_user_by_email(self, email: str) -> dict | None:
        """Возвращает строку пользователя по email или None, если не найден."""
        try:
            self.db_manager.execute(
                "SELECT id, name, email, status FROM users WHERE email = %s LIMIT 1",
                (email,),
            )
            row = self.db_manager.fetchone()
            if row is None:
                return None
            return {"id": row[0], "name": row[1], "email": row[2], "status": row[3]}
        except Exception as e:
            logger.exception(f"Failed to fetch user by email {email}")
            message = f"DB query failed: {e}"
            raise RuntimeError(message) from e

    def set_user_status(self, user_id: int, status: str) -> None:
        """Меняет статус пользователя напрямую в БД. Используется, когда через API это недоступно."""
        try:
            self.db_manager.execute(
                "UPDATE users SET status = %s WHERE id = %s",
                (status, user_id),
            )
            self.db_manager.commit()
            logger.info(f"User {user_id} status set to {status} via DB")
        except Exception as e:
            self.db_manager.rollback()
            message = f"Failed to update user {user_id} status: {e}"
            raise RuntimeError(message) from e

    def insert_user(self, user_id: int, name: str, email: str, status: str) -> None:
        """Добавляет строку пользователя, как это сделало бы реальное приложение при регистрации."""
        try:
            self.db_manager.execute(
                """
                INSERT INTO users (id, name, email, status) VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, email = EXCLUDED.email, status = EXCLUDED.status
                """,
                (user_id, name, email, status),
            )
            self.db_manager.commit()
        except Exception as e:
            self.db_manager.rollback()
            message = f"Failed to insert user {user_id}: {e}"
            raise RuntimeError(message) from e

    def delete_user(self, user_id: int) -> None:
        """Удаляет строку пользователя по id."""
        try:
            self.db_manager.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.db_manager.commit()
        except Exception as e:
            self.db_manager.rollback()
            message = f"Failed to delete user {user_id}: {e}"
            raise RuntimeError(message) from e

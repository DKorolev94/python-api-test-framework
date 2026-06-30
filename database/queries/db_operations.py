from database.connectors.postgres_connector import DatabaseManager
from utils.logger import get_logger

logger = get_logger(__name__)


class DBOperation:
    """Domain-specific DB queries.

    Use only when data cannot be obtained via API.
    Each method is one atomic operation — commit on success, rollback on error.
    Always use %s placeholders, never f-strings in SQL.
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_user_by_email(self, email: str) -> dict | None:
        """Returns user row by email, or None if not found."""
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
            logger.error(f"Failed to fetch user by email {email}: {e}")
            raise RuntimeError(f"DB query failed: {e}") from e

    def set_user_status(self, user_id: int, status: str) -> None:
        """Updates user status directly in DB. Use when API does not expose this."""
        try:
            self.db_manager.execute(
                "UPDATE users SET status = %s WHERE id = %s",
                (status, user_id),
            )
            self.db_manager.commit()
            logger.info(f"User {user_id} status set to {status} via DB")
        except Exception as e:
            self.db_manager.rollback()
            raise RuntimeError(f"Failed to update user {user_id} status: {e}") from e

import sqlite3
from sqlite3 import IntegrityError

from app.core.logger import logger
from app.core.paths import database_file


class DatabaseOperator:
    def __init__(self):
        self._db = database_file

    def get_status(self, thread_id: str) -> str | None:
        with sqlite3.connect(self._db) as conn:
            res = conn.execute(
                "SELECT status FROM users WHERE thread_id = ? LIMIT 1",
                (thread_id,)
            )
            rows = res.fetchall()
            if rows:
                return rows[0][0]
            return None

    def create_user(self, thread_id: str) -> None:
        try:
            with sqlite3.connect(self._db) as conn:
                conn.execute(
                    "INSERT INTO users (thread_id, status) VALUES (?, ?)",
                    (thread_id, "new")
                )
        except IntegrityError:
            logger.warning(f"User with {thread_id} thread ID already in database.")

    def update_status(self, thread_id: str, new_status: str) -> None:
        with sqlite3.connect(self._db) as conn:
            res = conn.execute(
                "UPDATE users SET status = ? WHERE thread_id = ?",
                (new_status, thread_id)
            )
            if res.rowcount == 0:
                logger.warning(f"No user with {thread_id} in database.")

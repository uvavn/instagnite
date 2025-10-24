import sqlite3
from pathlib import Path

DATABASE = Path.cwd() / "targets.db"

def create_database(database: Path = DATABASE) -> None:
    if not database.exists():
        with sqlite3.connect(database) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS users (thread_id TEXT UNIQUE, status TEXT)")

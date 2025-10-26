import sqlite3
from pathlib import Path
from app.core.paths import database_file

def create_database(database: Path = database_file) -> None:
    if not database.exists():
        with sqlite3.connect(database) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS users (thread_id TEXT UNIQUE, status TEXT)")

from pathlib import Path
import sqlite3

BASE_DIR = Path.cwd()
SETTINGS_DIR = BASE_DIR / 'settings'
DATABASE_PATH = BASE_DIR / "db.sqlite"


def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as conn:
        with open(SETTINGS_DIR / "createTables.sql", "r", encoding="utf-8") as file:
            conn.executescript(file.read())
        conn.commit()


def get_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()

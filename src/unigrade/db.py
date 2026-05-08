"""Database utilities for unigrade.

This module provides simple utilities to initialize and access the SQLite
database used by the unigrade CLI.

Functions
    get_db_path: Return the filesystem path for the application's database.
    init_db: Create the database and required tables if they do not exist.
    get_db: Context manager that yields an open sqlite3.Connection.
"""

import sqlite3
from contextlib import contextmanager
from typing import Iterator

from platformdirs import user_data_dir

APP_NAME = "unigrade"
DB_NAME = "unigrade.db"


def get_db_path() -> str:
    app_data_dir = user_data_dir(APP_NAME, ensure_exists=True)
    return f"{app_data_dir}/{DB_NAME}"


def init_db(db_path: str | None = None) -> None:
    """Initializes the database with required tables.

    Creates the grades and settings tables if they don't already exist.

    Args:
        db_path: Optional path to the database file. If None, uses the default
            database path from get_db_path().
    """
    if db_path is None:
        db_path = get_db_path()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grade REAL NOT NULL,
                credits INTEGER NOT NULL,
                course TEXT NOT NULL,
                semester TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                worst_grade REAL NOT NULL,
                best_grade REAL NOT NULL,
                pass_grade REAL NOT NULL,
                degree_credits INTEGER NOT NULL
                    CHECK (degree_credits > 0)
            )
        """
        )
        conn.commit()


@contextmanager
def get_db(db_path: str | None = None) -> Iterator[sqlite3.Connection]:
    """Provides an SQLite database connection.

    Ensures the database is initialized before opening a connection and closes
    the connection on context exit.

    Args:
        db_path: Optional path to the database file. If None, uses the default
            database path from get_db_path().

    Yields:
        sqlite3.Connection: An open SQLite connection.
    """
    if db_path is None:
        db_path = get_db_path()

    init_db(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allow accessing columns by name

    try:
        yield conn
    finally:
        conn.close()

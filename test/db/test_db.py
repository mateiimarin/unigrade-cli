"""Tests for the database utilities in unigrade.db."""

import sqlite3
from pathlib import Path

from unigrade import db


def test_get_path_returns_valid_path():
    db_path = db.get_path()
    assert isinstance(db_path, str)
    assert db_path.endswith("unigrade.db")


def test_init_db_creates_tables():
    db.init()
    db_path = db.get_path()

    # Check if .db file was created
    assert Path(db_path).exists()

    # Check if DB contains correct tables
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        tables = cursor.execute(
            "SELECT name FROM sqlite_schema WHERE type='table'"
        ).fetchall()
        tables_names = {table["name"] for table in tables}

        assert "grades" in tables_names
        assert "settings" in tables_names

    # Check if tables have correct columns
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        grades_columns = cursor.execute("PRAGMA table_info(grades)").fetchall()
        grades_column_names = {col["name"] for col in grades_columns}
        assert {
            "id",
            "grade",
            "credits",
            "course",
            "semester",
            "created_at",
        }.issubset(grades_column_names)

        settings_columns = cursor.execute(
            "PRAGMA table_info(settings)"
        ).fetchall()
        settings_column_names = {col["name"] for col in settings_columns}
        assert {
            "id",
            "worst_grade",
            "best_grade",
            "pass_grade",
            "degree_credits",
        }.issubset(settings_column_names)


def test_get_db_returns_valid_connection():
    with db.get(db.get_path()) as conn:
        assert isinstance(conn, sqlite3.Connection)

        # Check if connection can execute a query
        conn.execute(
            """INSERT INTO grades (grade, credits, course, semester)
                VALUES (?, ?, ?, ?)""",
            (5.25, 7, "AlgDat", "HS24"),
        )
        row = conn.execute("SELECT * FROM grades").fetchone()

        assert row["grade"] == 5.25
        assert row["course"] == "AlgDat"

"""Tests for the database utilities in unigrade.db."""

import sqlite3
from pathlib import Path

import pytest

from unigrade.db import get_db, get_db_path, init_db


@pytest.fixture(name="temp_db_path")
def fixture_temp_db_path(tmp_path) -> str:
    return str(tmp_path / "test_unigrade.db")


def test_get_db_path_returns_valid_path(monkeypatch, tmp_path):
    fake_dir = tmp_path / "appdata"
    monkeypatch.setattr(
        "unigrade.db.user_data_dir", lambda *args, **kwargs: str(fake_dir)
    )
    path = get_db_path()
    assert isinstance(path, str)
    assert path.endswith("unigrade.db")


def test_init_db_creates_tables(temp_db_path):
    init_db(temp_db_path)

    # Check if .db file was created
    assert Path(temp_db_path).exists()

    # Check if DB contains correct tables
    with sqlite3.connect(temp_db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        tables = cursor.execute(
            "SELECT name FROM sqlite_schema WHERE type='table'"
        ).fetchall()
        tables_names = {table["name"] for table in tables}

        assert "grades" in tables_names
        assert "settings" in tables_names

    # Check if tables have correct columns
    with sqlite3.connect(temp_db_path) as conn:
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
            "min_grade",
            "max_grade",
            "pass_grade",
            "higher_is_better",
            "degree_credits",
        }.issubset(settings_column_names)


def test_get_db_returns_valid_connection(temp_db_path):
    with get_db(temp_db_path) as conn:
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

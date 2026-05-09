"""Provide fixtures for the entire test suite."""

import pytest


@pytest.fixture(autouse=True)
def mock_db_path(monkeypatch, tmp_path) -> None:
    """
    Automatically mock the database path for all tests.
    This ensures no test can touch the real database.
    """
    temp_db_path = tmp_path / "test_unigrade.db"

    # Force get_path to return the path to the mock database
    monkeypatch.setattr("unigrade.db.get_path", lambda: str(temp_db_path))

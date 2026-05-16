"""Database storage layer for grading settings.

This module provides functions to handle the storage, retrieval, and updating
of grading settings in the underlying SQLite database.
"""

from dataclasses import asdict

from unigrade import db
from unigrade.models.settings import GradingSettings, GradingSettingsUpdate

SETTINGS_ENTRY_ID = 1  # Only one settings record, so we can use a fixed ID


def save(settings: GradingSettings) -> None:
    """Sets or replaces the grading settings in the database.

    Args:
        settings: A GradingSettings instance containing the values to persist.
    """

    data = asdict(settings)
    with db.get() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO settings (id, worst_grade, best_grade,
                       pass_grade, degree_credits)
            VALUES (:id, :worst_grade, :best_grade, :pass_grade,
                       :degree_credits)
        """,
            {**data, "id": SETTINGS_ENTRY_ID},
        )

        conn.commit()


def get() -> GradingSettings | None:
    """Retrieves the grading settings from the database.

    Returns:
        A GradingSettings object if a record exists, otherwise None.
    """
    with db.get() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM settings WHERE id = ?", (SETTINGS_ENTRY_ID,)
        )
        settings = cursor.fetchone()
        if settings:
            columns = [
                "worst_grade",
                "best_grade",
                "pass_grade",
                "degree_credits",
            ]
            data = {col: settings[col] for col in columns}
            return GradingSettings(**data)
        return None


def update(settings: GradingSettingsUpdate) -> None:
    """Updates specific fields of the grading settings.

    Only fields that are not None in the settings object will be updated.

    Args:
        settings: A GradingSettingsUpdate instance containing fields
          to update.
    """
    # Keep only the fields with updates (non-None values)
    update_data = {k: v for k, v in asdict(settings).items() if v is not None}

    if not update_data:
        return

    # Construct SQL query using named parameters
    # eg. (worst_grade = :worst_grade, etc.)
    set_query = ", ".join([f"{k} = :{k}" for k in update_data.keys()])
    query = f"UPDATE settings SET {set_query} WHERE id = :id"

    with db.get() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {**update_data, "id": SETTINGS_ENTRY_ID})

        conn.commit()

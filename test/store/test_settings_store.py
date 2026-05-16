"""Tests for the grading settings store layer"""

import pytest

from unigrade.models.settings import GradingSettings, GradingSettingsUpdate
from unigrade.store import settings_store


@pytest.fixture(name="sample_settings")
def fixture_sample_settings() -> list[GradingSettings]:
    """Provides sample grading settings for testing."""
    return [
        GradingSettings(
            worst_grade=1.0, best_grade=6.0, pass_grade=4.0, degree_credits=180
        ),
        GradingSettings(
            worst_grade=1.0, best_grade=10.0, pass_grade=6.0, degree_credits=240
        ),
    ]


def test_get_returns_none_when_no_settings():
    assert settings_store.get() is None


def test_save_and_get(sample_settings):
    settings_store.save(sample_settings[0])
    retrieved_settings = settings_store.get()
    assert retrieved_settings == sample_settings[0]


def test_save_replaces_existing_settings(sample_settings):
    settings_store.save(sample_settings[0])
    settings_store.save(sample_settings[1])

    retrieved_settings = settings_store.get()
    assert retrieved_settings == sample_settings[1]


def test_update_modifies_fields(sample_settings):
    initial_settings = sample_settings[0]
    settings_store.save(initial_settings)

    update_data = GradingSettingsUpdate(
        degree_credits=240, best_grade=10.0, pass_grade=6.0
    )

    settings_store.update(update_data)

    retrieved_settings = settings_store.get()
    assert retrieved_settings.best_grade == update_data.best_grade
    assert retrieved_settings.pass_grade == update_data.pass_grade
    assert retrieved_settings.degree_credits == update_data.degree_credits
    assert retrieved_settings.worst_grade == initial_settings.worst_grade

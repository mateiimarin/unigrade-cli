"""Tests for grading settings models."""

import pytest

from unigrade.exceptions import ValidationError
from unigrade.models.settings import GradingSettings, GradingSettingsUpdate


def test_gradingsettings_valid_init():
    settings = GradingSettings(
        worst_grade=1.0, best_grade=6.0, pass_grade=4.0, degree_credits=180
    )
    assert settings.worst_grade == 1.0
    assert settings.best_grade == 6.0
    assert settings.pass_grade == 4.0
    assert settings.degree_credits == 180


@pytest.mark.parametrize(
    """worst_grade, best_grade, pass_grade,
                         degree_credits, message""",
    [
        (-1.0, 6.0, 4.0, 180, "Worst grade must be non-negative."),
        (1.0, -1.0, 4.0, 180, "Best grade must be non-negative."),
        (1.0, 6.0, -1.0, 180, "Passing grade must be non-negative."),
        (1.0, 6.0, 4.0, -1, "Number of degree credits must be non-negative."),
    ],
)
def test_gradingsettings_validation_errors(
    worst_grade, best_grade, pass_grade, degree_credits, message
):
    with pytest.raises(ValidationError) as err:
        GradingSettings(
            worst_grade=worst_grade,
            best_grade=best_grade,
            pass_grade=pass_grade,
            degree_credits=degree_credits,
        )
    assert err.value.message == message


def test_gradingsettingsupdate_valid_init():
    update = GradingSettingsUpdate(worst_grade=4.0, degree_credits=180)
    assert update.worst_grade == 4.0
    assert update.best_grade is None
    assert update.pass_grade is None
    assert update.degree_credits == 180


@pytest.mark.parametrize(
    "update_kwargs, message",
    [
        ({"worst_grade": -1.0}, "Worst grade must be non-negative."),
        ({"best_grade": -1.0}, "Best grade must be non-negative."),
        ({"pass_grade": -1.0}, "Passing grade must be non-negative."),
        (
            {"degree_credits": -1},
            "Number of degree credits must be non-negative.",
        ),
    ],
)
def test_gradingsettingsupdate_validation_errors(update_kwargs, message):
    with pytest.raises(ValidationError) as err:
        GradingSettingsUpdate(**update_kwargs)
    assert err.value.message == message

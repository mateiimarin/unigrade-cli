"""Data models for grading settings.

This module defines dataclasses used to represent the grading settings and
updates to those settings.

"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GradingSettings:
    """Represents the grading settings for the user.

    Contains information about the grading scale and degree requirements.
    Should be used for initializing/reading the settings.

    Attributes:
        worst_grade: The value representing the worst performance on the
            grading scale.
        best_grade: The value representing the best performance on the
            grading scale.
        pass_grade: The minimum grade required to pass a course.
        degree_credits: The total number of credits required to complete
            the degree.
    """

    worst_grade: float
    best_grade: float
    pass_grade: float
    degree_credits: int

    def __post_init__(self):
        self.__validate()

    def __validate(self) -> None:
        if self.worst_grade < 0:
            raise ValueError("worst_grade must be non-negative.")
        if self.best_grade < 0:
            raise ValueError("best_grade must be non-negative.")
        if self.degree_credits < 0:
            raise ValueError("degree_credits must be non-negative.")


@dataclass(frozen=True)
class GradingSettingsUpdate:
    """Represents an update to the grading settings.

    Contains optional fields for updating the grading scale and degree
    requirements. Should be used for updating existing settings.

    Attributes:
        worst_grade: Optional new value for the worst performance on the
            grading scale.
        best_grade: Optional new value for the best performance on the
            grading scale.
        pass_grade: Optional new value for the minimum grade required to pass
            a course.
        degree_credits: Optional new value for the total number of credits
            required to complete the degree.
    """

    worst_grade: float | None = None
    best_grade: float | None = None
    pass_grade: float | None = None
    degree_credits: int | None = None

    def __post_init__(self):
        self.__validate()

    def __validate(self) -> None:
        if self.worst_grade is not None and self.worst_grade < 0:
            raise ValueError("worst_grade must be non-negative.")
        if self.best_grade is not None and self.best_grade < 0:
            raise ValueError("best_grade must be non-negative.")
        if self.degree_credits is not None and self.degree_credits < 0:
            raise ValueError("degree_credits must be non-negative.")

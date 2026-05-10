"""Custom exceptions."""


class UnigradeError(Exception):
    """Base exception for unigrade."""

    def __init__(self, message: str, hint: str | None = None):
        self.message = message
        self.hint = hint


class NotFoundError(UnigradeError):
    """Raised when a requested resource is not found."""

    pass


class ValidationError(UnigradeError):
    """Raised when input data fails validation."""

    pass

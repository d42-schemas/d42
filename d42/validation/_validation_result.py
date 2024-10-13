from typing import List, Optional

from .errors import ValidationError

__all__ = ("ValidationResult",)


class ValidationResult:
    def __init__(self, errors: Optional[List[ValidationError]] = None) -> None:
        self._errors = errors if (errors is not None) else []

    def add_error(self, error: ValidationError) -> "ValidationResult":
        self._errors.append(error)
        return self

    def add_errors(self, errors: List[ValidationError]) -> "ValidationResult":
        for error in errors:
            self._errors.append(error)
        return self

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def get_errors(self) -> List[ValidationError]:
        return self._errors

    def __repr__(self) -> str:
        errors = repr(self._errors) if self.has_errors() else ""
        return f"{self.__class__.__name__}({errors})"

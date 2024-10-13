from os import linesep

from d42.validation import Formatter, ValidationResult

__all__ = ("SubstitutionError", "make_substitution_error",)


class SubstitutionError(Exception):
    pass


def make_substitution_error(result: ValidationResult, formatter: Formatter) -> SubstitutionError:
    errors = [e.format(formatter) for e in result.get_errors()]
    message = f"{linesep} - " + f"{linesep} - ".join(errors)
    return SubstitutionError(message)

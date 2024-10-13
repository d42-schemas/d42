from baby_steps import given, then, when
from th import PathHolder

from d42.validation import ValidationResult
from d42.validation.errors import TypeValidationError, ValidationError


def make_error() -> ValidationError:
    return TypeValidationError(PathHolder(), "", int)


def test_validation_result():
    with when:
        result = ValidationResult()

    with then:
        assert result.get_errors() == []
        assert not result.has_errors()


def test_validation_result_with_errors():
    with given:
        errors = [make_error(), make_error()]

    with when:
        result = ValidationResult(errors)

    with then:
        assert result.get_errors() == errors
        assert result.has_errors()


def test_validation_result_add_error():
    with given:
        result = ValidationResult()
        error = make_error()

    with when:
        result = result.add_error(error)

    with then:
        assert result.get_errors() == [error]
        assert result.has_errors()


def test_validation_result_add_errors():
    with given:
        result = ValidationResult()
        errors = [make_error(), make_error()]

    with when:
        result = result.add_errors(errors)

    with then:
        assert result.get_errors() == errors
        assert result.has_errors()


def test_validation_result_repr():
    with given:
        result = ValidationResult()

    with when:
        res = repr(result)

    with then:
        assert res == "ValidationResult()"


def test_validation_result_with_errors_repr():
    with given:
        errors = [make_error(), make_error()]
        result = ValidationResult(errors)

    with when:
        res = repr(result)

    with then:
        assert res == f"ValidationResult({errors!r})"

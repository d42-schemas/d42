from baby_steps import then, when
from pytest import raises

from d42 import schema, validate, validate_or_fail
from d42.validation import ValidationException, ValidationResult, eq


def test_validator_validate_pass():
    with when:
        result = validate(schema.int, 42)

    with then:
        assert isinstance(result, ValidationResult)
        assert not result.has_errors()


def test_validator_validate_fail():
    with when:
        result = validate(schema.int, "42")

    with then:
        assert isinstance(result, ValidationResult)
        assert result.has_errors()


def test_validator_validate_or_fail():
    with when:
        result = validate_or_fail(schema.int, 42)

    with then:
        assert result is True


def test_validator_validate_or_fail_error():
    with when, raises(Exception) as exception:
        validate_or_fail(schema.dict, "")

    with then:
        assert exception.type is ValidationException
        assert str(exception.value) == ("\n - Value '' must be <class 'dict'>, "
                                        "but <class 'str'> given")


def test_validator_validate_or_fail_multiline():
    with when, raises(Exception) as exception:
        validate_or_fail(schema.dict({"id": schema.int, "name": schema.str}), {})

    with then:
        assert exception.type is ValidationException
        assert str(exception.value) == ("\n - Key _['id'] does not exist"
                                        "\n - Key _['name'] does not exist")


def test_validator_eq():
    with when:
        result = eq(schema.str, schema.str)

    with then:
        assert result is True


def test_validator_not_eq_schema():
    with when:
        result = eq(schema.str, schema.int)

    with then:
        assert result is False


def test_validator_not_eq_props():
    with when:
        result = eq(schema.str, schema.str.len(1))

    with then:
        assert result is False


def test_validator_not_eq_value():
    with when:
        result = eq(schema.str, 42)

    with then:
        assert result is False

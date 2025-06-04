from baby_steps import given, then, when
from pytest import raises

from d42 import schema, validate_or_fail
from d42.validation import ValidationException


def test_validate_or_fail_with_unique_list():
    with given:
        unique_schema = schema.list(schema.int).unique()
        unique_list = [1, 2, 3, 4, 5]

    with when:
        result = validate_or_fail(unique_schema, unique_list)

    with then:
        assert result is True


def test_validate_or_fail_with_non_unique_list():
    with given:
        unique_schema = schema.list(schema.int).unique()
        duplicate_list = [1, 2, 3, 3, 5]

    with when, raises(ValidationException) as exception:
        validate_or_fail(unique_schema, duplicate_list)

    with then:
        assert "unique" in str(exception.value).lower()


def test_validate_or_fail_with_mixed_types_unique_list():
    with given:
        mixed_schema = schema.list(schema.any(
            schema.str,
            schema.int,
            schema.bool
        )).unique()
        mixed_unique = ["a", 1, False, "b", 2]

    with when:
        result = validate_or_fail(mixed_schema, mixed_unique)

    with then:
        assert result is True


def test_validate_or_fail_with_mixed_types_non_unique_list():
    with given:
        mixed_schema = schema.list(schema.any(
            schema.str,
            schema.int,
            schema.bool
        )).unique()
        mixed_duplicate = ["a", 1, False, "a", 2]

    with when, raises(ValidationException) as exception:
        validate_or_fail(mixed_schema, mixed_duplicate)

    with then:
        assert "unique" in str(exception.value).lower()

import uuid

import pytest
from baby_steps import given, then, when
from th import PathHolder, _

from d42 import schema
from d42.validation import Formatter
from d42.validation.errors import (
    AlphabetValidationError,
    ExtraElementValidationError,
    ExtraKeyValidationError,
    InvalidUUIDVersionValidationError,
    LengthValidationError,
    MaxLengthValidationError,
    MaxValueValidationError,
    MinLengthValidationError,
    MinValueValidationError,
    MissingElementValidationError,
    MissingKeyValidationError,
    RegexValidationError,
    SchemaMismatchValidationError,
    SubstrValidationError,
    TypeValidationError,
    ValueValidationError,
)


@pytest.fixture()
def formatter() -> Formatter:
    return Formatter()


def test_formatter_default_root():
    with when:
        formatter = Formatter()

    with then:
        assert formatter.root == "_"


def test_formatter_custom_root():
    with when:
        formatter = Formatter("#")

    with then:
        assert formatter.root == "#"


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value 'banana' must be <class 'int'>, but <class 'str'> given"),
    (_["id"], "Value 'banana' at _['id'] must be <class 'int'>, but <class 'str'> given")
])
def test_format_type_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = TypeValidationError(path, actual_value="banana", expected_type=int)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must be equal to 'banana', but 'orange' given"),
    (_["id"], "Value <class 'str'> at _['id'] must be equal to 'banana', but 'orange' given")
])
def test_format_value_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = ValueValidationError(path, actual_value="orange", expected_value="banana")

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'int'> must be greater than or equal to 1, but 0 given"),
    (_["id"], "Value <class 'int'> at _['id'] must be greater than or equal to 1, but 0 given")
])
def test_format_min_value_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = MinValueValidationError(path, actual_value=0, min_value=1)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'int'> must be less than or equal to 0, but 1 given"),
    (_["id"], "Value <class 'int'> at _['id'] must be less than or equal to 0, but 1 given")
])
def test_format_max_value_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = MaxValueValidationError(path, actual_value=1, max_value=0)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must have exactly 1 element, but it has 2 elements"),
    (_["id"], "Value <class 'str'> at _['id'] must have exactly 1 element, but it has 2 elements")
])
def test_format_length_one_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = LengthValidationError(path, actual_value="ab", length=1)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must have exactly 2 elements, but it has 1 element"),
    (_["id"], "Value <class 'str'> at _['id'] must have exactly 2 elements, but it has 1 element")
])
def test_format_length_many_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = LengthValidationError(path, actual_value="a", length=2)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must have at least 1 element, but it has 0 elements"),
    (_["id"], "Value <class 'str'> at _['id'] must have at least 1 element, but it has 0 elements")
])
def test_format_min_length_one_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = MinLengthValidationError(path, actual_value="", min_length=1)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must have at least 3 elements, but it has 1 element"),
    (_["id"], "Value <class 'str'> at _['id'] must have at least 3 elements, but it has 1 element")
])
def test_format_min_length_many_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = MinLengthValidationError(path, actual_value="a", min_length=3)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must have at most 1 element, but it has 2 elements"),
    (_["id"], "Value <class 'str'> at _['id'] must have at most 1 element, but it has 2 elements")
])
def test_format_max_length_one_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = MaxLengthValidationError(path, actual_value="ab", max_length=1)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must have at most 0 elements, but it has 1 element"),
    (_["id"], "Value <class 'str'> at _['id'] must have at most 0 elements, but it has 1 element")
])
def test_format_max_length_many_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = MaxLengthValidationError(path, actual_value="a", max_length=0)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must contain only '0123456789', but 'banana' given"),
    (_["id"], "Value <class 'str'> at _['id'] must contain only '0123456789', but 'banana' given")
])
def test_format_alphabet_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = AlphabetValidationError(path, actual_value="banana", alphabet="0123456789")

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must contain 'banana', but 'ananab' given"),
    (_["id"], "Value <class 'str'> at _['id'] must contain 'banana', but 'ananab' given")
])
def test_format_substr_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = SubstrValidationError(path, actual_value="ananab", substr="banana")

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'str'> must match pattern '[0-9]+', but 'banana' given"),
    (_["id"], "Value <class 'str'> at _['id'] must match pattern '[0-9]+', but 'banana' given")
])
def test_format_regex_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = RegexValidationError(path, actual_value="banana", pattern="[0-9]+")

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Element _[1] does not exist"),
    (_["id"], "Element _['id'][1] does not exist")
])
def test_format_missing_element_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = MissingElementValidationError(path, actual_value=["a"], index=1)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value contains extra element at index 1"),
    (_["id"], "Value at _['id'] contains extra element at index 1")
])
def test_format_extra_element_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = ExtraElementValidationError(path, actual_value=["a", "b"], index=1)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Key _['missing_key'] does not exist"),
    (_["id"], "Key _['id']['missing_key'] does not exist")
])
def test_format_missing_key_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = MissingKeyValidationError(path, actual_value={}, missing_key="missing_key")

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value contains extra key 'extra_key'"),
    (_["id"], "Value at _['id'] contains extra key 'extra_key'")
])
def test_format_extra_key_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        value = {"extra_key": "value"}
        error = ExtraKeyValidationError(path, actual_value=value, extra_key="extra_key")

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'int'> must match any of (schema.str, schema.none), but 42 given"),
    (_["id"], "Value <class 'int'> at _['id'] must match any of (schema.str, schema.none), "
              "but 42 given"),
])
def test_format_schema_missmatch_error(path: PathHolder, formatted: str, *, formatter: Formatter):
    with given:
        error = SchemaMismatchValidationError(path, actual_value=42,
                                              expected_schemas=(schema.str, schema.none))

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


@pytest.mark.parametrize(("path", "formatted"), [
    (_, "Value <class 'uuid.UUID'> must be a UUID version 4, "
        "but UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d') version 5 given"),
    (_["id"], "Value <class 'uuid.UUID'> at _['id'] must be a UUID version 4, "
              "but UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d') version 5 given"),
])
def test_format_invalid_uuid_version_error(path: PathHolder, formatted: str, *,
                                           formatter: Formatter):
    with given:
        uuid5 = uuid.UUID("886313e1-3b8a-5372-9b90-0c9aee199e5d", version=5)
        error = InvalidUUIDVersionValidationError(path, actual_value=uuid5, actual_version=5,
                                                  expected_version=4)

    with when:
        res = error.format(formatter)

    with then:
        assert res == formatted


def test_format_any_schema_missmatch_error(*, formatter: Formatter):
    with given:
        value = 3.14
        error = SchemaMismatchValidationError(
            PathHolder(),
            value,
            (schema.none, schema.str, schema.int),
            [
                (0, [TypeValidationError(PathHolder(), value, type(None))]),
                (1, [TypeValidationError(PathHolder(), value, str)]),
                (2, [TypeValidationError(PathHolder(), value, int)])
            ]
        )

    with when:
        res = error.format(formatter)

    with then:
        expected = (
            "Value at _ does not match any of the allowed schemas:\n"
            " | Schema 1:\n"
            " |   - Value 3.14 must be <class 'NoneType'>, but <class 'float'> given\n"
            " | Schema 2:\n"
            " |   - Value 3.14 must be <class 'str'>, but <class 'float'> given\n"
            " | Schema 3:\n"
            " |   - Value 3.14 must be <class 'int'>, but <class 'float'> given"
        )
        assert res == expected


def test_format_any_schema_with_nested_schemas_missmatch_error(*, formatter: Formatter):
    with given:
        value = 3.14
        nested_error = SchemaMismatchValidationError(
            PathHolder(),
            value,
            (schema.str, schema.int),
            [
                (0, [TypeValidationError(PathHolder(), value, str)]),
                (1, [TypeValidationError(PathHolder(), value, int)])
            ]
        )
        error = SchemaMismatchValidationError(
            PathHolder(),
            value,
            (schema.none, schema.dict({"type": schema.str})),
            [
                (0, [TypeValidationError(PathHolder(), value, type(None))]),
                (1, [nested_error])
            ]
        )

    with when:
        res = error.format(formatter)

    with then:
        expected = (
            "Value at _ does not match any of the allowed schemas:\n"
            " | Schema 1:\n"
            " |   - Value 3.14 must be <class 'NoneType'>, but <class 'float'> given\n"
            " | Schema 2:\n"
            " |   - Value at _ does not match any of the allowed schemas:\n"
            " |   -  |    | Schema 2.1:\n"
            " |   -  |    |   - Value 3.14 must be <class 'str'>, but <class 'float'> given\n"
            " |   -  |    | Schema 2.2:\n"
            " |   -  |    |   - Value 3.14 must be <class 'int'>, but <class 'float'> given"
        )
        assert res == expected

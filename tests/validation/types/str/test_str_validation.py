import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import (
    AlphabetValidationError,
    LengthValidationError,
    MaxLengthValidationError,
    MinLengthValidationError,
    RegexValidationError,
    SubstrValidationError,
    TypeValidationError,
    ValueValidationError,
)


def test_str_type_validation():
    with when:
        result = validate(schema.str, "banana")

    with then:
        assert result.get_errors() == []


def test_str_type_validation_error():
    with given:
        value = ["b", "a", "n", "a", "n", "a"]

    with when:
        result = validate(schema.str, value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), value, str),
        ]


def test_str_value_validation():
    with given:
        value = "banana"

    with when:
        result = validate(schema.str(value), value)

    with then:
        assert result.get_errors() == []


def test_str_value_validation_error():
    with given:
        expected_value = "banana"
        actual_value = "cucumber"

    with when:
        result = validate(schema.str(expected_value), actual_value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), actual_value, expected_value),
        ]


def test_str_len_validation():
    with given:
        value = "banana"

    with when:
        result = validate(schema.str.len(6), value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize("value", [
    "banana",
    "banana!!"
])
def test_str_len_validation_error(value: str):
    with given:
        length = 7

    with when:
        result = validate(schema.str.len(length), value)

    with then:
        assert result.get_errors() == [
            LengthValidationError(PathHolder(), value, length),
        ]


@pytest.mark.parametrize("value", [
    "banana",
    "banana!",
])
def test_str_min_len_validation(value: str):
    with when:
        result = validate(schema.str.len(6, ...), value)

    with then:
        assert result.get_errors() == []


def test_str_min_len_validation_error():
    with given:
        value = "banana"
        min_length = 7

    with when:
        result = validate(schema.str.len(min_length, ...), value)

    with then:
        assert result.get_errors() == [
            MinLengthValidationError(PathHolder(), value, min_length),
        ]


@pytest.mark.parametrize("value", [
    "banana",
    "banana!",
])
def test_str_max_len_validation(value: str):
    with when:
        result = validate(schema.str.len(..., 7), value)

    with then:
        assert result.get_errors() == []


def test_str_max_len_validation_error():
    with given:
        value = "banana"
        max_length = 5

    with when:
        result = validate(schema.str.len(..., max_length), value)

    with then:
        assert result.get_errors() == [
            MaxLengthValidationError(PathHolder(), value, max_length)
        ]


@pytest.mark.parametrize(("min_length", "max_length"), [
    (6, 6),
    (5, 7),
])
def test_str_min_max_len_validation(min_length: int, max_length: int):
    with given:
        value = "banana"

    with when:
        result = validate(schema.str.len(min_length, max_length), value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize(("min_length", "max_length"), [
    (5, 5),
    (7, 7),
])
def test_str_min_max_len_validation_error(min_length: int, max_length: int):
    with given:
        value = "banana"

    with when:
        result = validate(schema.str.len(min_length, max_length), value)

    with then:
        assert len(result.get_errors()) == 1


@pytest.mark.parametrize("value", [
    "",
    "11",
    "1234567890",
])
def test_str_alphabet_validation(value: str):
    with when:
        result = validate(schema.str.alphabet("1234567890"), value)

    with then:
        assert result.get_errors() == []


def test_str_alphabet_validation_error():
    with given:
        value = "banana"
        alphabet = "1234567890"

    with when:
        result = validate(schema.str.alphabet(alphabet), value)

    with then:
        assert result.get_errors() == [
            AlphabetValidationError(PathHolder(), value, alphabet)
        ]


def test_str_len_alphabet_validation_error():
    with given:
        value = "banana"
        length = 7
        alphabet = "1234567890"

    with when:
        result = validate(schema.str.alphabet(alphabet).len(length), value)

    with then:
        assert result.get_errors() == [
            LengthValidationError(PathHolder(), value, length),
            AlphabetValidationError(PathHolder(), value, alphabet),
        ]


@pytest.mark.parametrize("value", [
    "banana",
    " banana",
    "banana ",
    " banana ",
])
def test_str_contains_validation(value: str):
    with given:
        substr = "banana"

    with when:
        result = validate(schema.str.contains(substr), value)

    with then:
        assert result.get_errors() == []


def test_str_contains_empty_validation():
    with given:
        value = "banana"
        substr = ""

    with when:
        result = validate(schema.str.contains(substr), value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize("value", [
    "",
    "ananab",
])
def test_str_contains_validation_error(value: str):
    with given:
        substr = "banana"

    with when:
        result = validate(schema.str.contains(substr), value)

    with then:
        assert result.get_errors() == [
            SubstrValidationError(PathHolder(), value, substr)
        ]


def test_str_regex_validation():
    with given:
        pattern = "[a-z]+"
        value = "banana"

    with when:
        result = validate(schema.str.regex(pattern), value)

    with then:
        assert result.get_errors() == []


def test_str_regex_validation_error():
    with given:
        pattern = "[0-9]+"
        value = "banana"

    with when:
        result = validate(schema.str.regex(pattern), value)

    with then:
        assert result.get_errors() == [
            RegexValidationError(PathHolder(), value, pattern)
        ]


def test_str_type_validation_kwargs():
    with given:
        expected_value = "banana"
        actual_value = "cucumber"
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.str(expected_value), actual_value, path=path)

    with then:
        assert result.get_errors() == [
            ValueValidationError(path, actual_value, expected_value)
        ]

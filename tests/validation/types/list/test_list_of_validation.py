from typing import Any, List

import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema, validate
from d42.validation.errors import (
    LengthValidationError,
    MaxLengthValidationError,
    MinLengthValidationError,
    TypeValidationError,
    ValueValidationError,
)


@pytest.mark.parametrize("value", [
    [],
    [1],
    [1, 2],
])
def test_list_of_elements_validation(value: Any):
    with when:
        result = validate(schema.list(schema.int), value)

    with then:
        assert result.get_errors() == []


def test_list_of_type_element_validation_error():
    with given:
        value = 3.14

    with when:
        result = validate(schema.list(schema.int), [value])

    with then:
        path = PathHolder()[0]
        assert result.get_errors() == [TypeValidationError(path, value, int)]


def test_list_of_type_elements_validation_error():
    with given:
        value = 3.14

    with when:
        result = validate(schema.list(schema.int), [42, value])

    with then:
        path = PathHolder()[1]
        assert result.get_errors() == [TypeValidationError(path, value, int)]


def test_list_of_type_element_value_validation_error():
    with given:
        expected_value = 42
        actual_value = 43

    with when:
        result = validate(schema.list(schema.int(expected_value)), [actual_value])

    with then:
        path = PathHolder()[0]
        assert result.get_errors() == [ValueValidationError(path, actual_value, expected_value)]


def test_list_of_type_elements_value_validation_error():
    with given:
        expected_value = 42
        actual_value = 43

    with when:
        result = validate(schema.list(schema.int(expected_value)), [expected_value, actual_value])

    with then:
        path = PathHolder()[1]
        assert result.get_errors() == [ValueValidationError(path, actual_value, expected_value)]


def test_list_of_len_validation():
    with given:
        value = [1, 2]

    with when:
        result = validate(schema.list(schema.int).len(2), value)

    with given:
        assert result.get_errors() == []


@pytest.mark.parametrize("value", [
    [1],
    [1, 2, 3],
])
def test_list_of_len_validation_error(value: List[Any]):
    with given:
        length = 2

    with when:
        result = validate(schema.list(schema.int).len(length), value)

    with then:
        assert result.get_errors() == [
            LengthValidationError(PathHolder(), value, length)
        ]


@pytest.mark.parametrize("value", [
    [1, 2],
    [1, 2, 3],
])
def test_list_of_min_len_validation(value: List[Any]):
    with when:
        result = validate(schema.list(schema.int).len(2, ...), value)

    with given:
        assert result.get_errors() == []


def test_list_of_min_len_validation_error():
    with given:
        value = [1]
        min_length = 2

    with when:
        result = validate(schema.list(schema.int).len(min_length, ...), value)

    with then:
        assert result.get_errors() == [
            MinLengthValidationError(PathHolder(), value, min_length)
        ]


@pytest.mark.parametrize("value", [
    [1, 2],
    [1],
])
def test_list_of_max_len_validation(value: List[Any]):
    with when:
        result = validate(schema.list(schema.int).len(..., 2), value)

    with given:
        assert result.get_errors() == []


def test_list_of_max_len_validation_error():
    with given:
        value = [1, 2, 3]
        max_length = 2

    with when:
        result = validate(schema.list(schema.int).len(..., max_length), value)

    with then:
        assert result.get_errors() == [
            MaxLengthValidationError(PathHolder(), value, max_length)
        ]


@pytest.mark.parametrize(("min_length", "max_length"), [
    (2, 2),
    (1, 3),
])
def test_list_of_min_max_len_validation(min_length: int, max_length: int):
    with given:
        value = [1, 2]

    with when:
        result = validate(schema.list(schema.int).len(min_length, max_length), value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize(("min_length", "max_length"), [
    (1, 1),
    (3, 3),
])
def test_list_of_min_max_len_validation_error(min_length: int, max_length: int):
    with given:
        value = [1, 2]

    with when:
        result = validate(schema.list(schema.int).len(min_length, max_length), value)

    with then:
        assert len(result.get_errors()) == 1


def test_list_of_type_validation_kwargs():
    with given:
        value = 3.14
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.list(schema.int), [42, value], path=path)

    with then:
        assert result.get_errors() == [
            TypeValidationError(path[1], value, int)
        ]

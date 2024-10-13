from typing import Any, List

import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema, validate
from d42.validation.errors import (
    ExtraElementValidationError,
    LengthValidationError,
    MaxLengthValidationError,
    MinLengthValidationError,
    MissingElementValidationError,
    TypeValidationError,
)


@pytest.mark.parametrize("value", [
    [],
    [1],
    [1, 2],
    [42, 3.14, "banana"],
])
def test_list_type_validation(value: List[Any]):
    with when:
        result = validate(schema.list, value)

    with then:
        assert result.get_errors() == []


def test_list_type_validation_error():
    with given:
        value = {}

    with when:
        result = validate(schema.list, value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), value, list),
        ]


def test_list_no_elements_validation():
    with when:
        result = validate(schema.list([]), [])

    with then:
        assert result.get_errors() == []


def test_list_homogeneous_elements_validation():
    with given:
        value = [1, 2]

    with when:
        result = validate(schema.list([
            schema.int(1),
            schema.int(2),
        ]), value)

    with then:
        assert result.get_errors() == []


def test_list_heterogeneous_elements_validation():
    with given:
        value = [42, 3.14, "banana"]

    with when:
        result = validate(schema.list([
            schema.int(42),
            schema.float(3.14),
            schema.str("banana"),
        ]), value)

    with then:
        assert result.get_errors() == []


def test_list_more_element_validation_error():
    with given:
        value = [1]

    with when:
        result = validate(schema.list([]), value)

    with then:
        assert result.get_errors() == [
            ExtraElementValidationError(PathHolder(), actual_value=value, index=0),
        ]


def test_list_more_elements_validation_error():
    with given:
        value = [1, 2, 3]

    with when:
        result = validate(schema.list([schema.int]), value)

    with then:
        assert result.get_errors() == [
            ExtraElementValidationError(PathHolder(), actual_value=value, index=1),
            ExtraElementValidationError(PathHolder(), actual_value=value, index=2),
        ]


def test_list_less_elements_validation_error():
    with given:
        value = [1, 2]

    with when:
        result = validate(schema.list([schema.int, schema.int, schema.int]), value)

    with then:
        assert result.get_errors() == [
            MissingElementValidationError(PathHolder(), actual_value=value, index=2),
        ]


def test_list_len_validation():
    with given:
        value = [1, 2]

    with when:
        result = validate(schema.list.len(2), value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize("value", [
    [1],
    [1, 2, 3],
])
def test_list_len_validation_error(value: List[Any]):
    with given:
        length = 2

    with when:
        result = validate(schema.list.len(length), value)

    with then:
        assert result.get_errors() == [
            LengthValidationError(PathHolder(), value, length)
        ]


@pytest.mark.parametrize("value", [
    [1, 2],
    [1, 2, 3],
])
def test_list_min_len_validation(value: List[Any]):
    with when:
        result = validate(schema.list.len(2, ...), value)

    with then:
        assert result.get_errors() == []


def test_list_min_len_validation_error():
    with given:
        value = [1]
        min_length = 2

    with when:
        result = validate(schema.list.len(min_length, ...), value)

    with then:
        assert result.get_errors() == [
            MinLengthValidationError(PathHolder(), value, min_length)
        ]


@pytest.mark.parametrize("value", [
    [1, 2],
    [1],
])
def test_list_max_len_validation(value: List[Any]):
    with when:
        result = validate(schema.list.len(..., 2), value)

    with then:
        assert result.get_errors() == []


def test_list_max_len_validation_error():
    with given:
        value = [1, 2, 3]
        max_length = 2

    with when:
        result = validate(schema.list.len(..., max_length), value)

    with then:
        assert result.get_errors() == [
            MaxLengthValidationError(PathHolder(), value, max_length)
        ]


@pytest.mark.parametrize(("min_length", "max_length"), [
    (2, 2),
    (1, 3),
])
def test_list_min_max_len_validation(min_length: int, max_length: int):
    with given:
        value = [1, 2]

    with when:
        result = validate(schema.list.len(min_length, max_length), value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize(("min_length", "max_length"), [
    (1, 1),
    (3, 3),
])
def test_list_min_max_len_validation_error(min_length: int, max_length: int):
    with given:
        value = [1, 2]

    with when:
        result = validate(schema.list.len(min_length, max_length), value)

    with then:
        assert len(result.get_errors()) == 1

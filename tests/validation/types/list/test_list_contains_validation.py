from typing import Any, List

import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema, validate
from d42.validation.errors import MissingElementValidationError, ValueValidationError


@pytest.mark.parametrize("value", [
    [],
    [1],
    [1, 2],
])
def test_list_contains_validation(value: List[Any]):
    with given:
        sch = schema.list([...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize("value", [
    [1, 2],
    [1, 2, 3],
    [1, 2, 3, 4],
])
def test_list_contains_head_validation(value: List[Any]):
    with given:
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_list_contains_head_validation_incorrect_element_error():
    with given:
        value = [2]
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()[0], actual_value=value[0], expected_value=1),
            MissingElementValidationError(PathHolder(), actual_value=value, index=1)
        ]


def test_list_contains_head_validation_missing_element_error():
    with given:
        value = [1]
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            MissingElementValidationError(PathHolder(), actual_value=value, index=1)
        ]


def test_list_contains_head_validation_error_extra_element():
    with given:
        value = [0, 1, 2]
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()[0], actual_value=value[0], expected_value=1),
            ValueValidationError(PathHolder()[1], actual_value=value[1], expected_value=2),
        ]


@pytest.mark.parametrize("value", [
    [1, 2],
    [0, 1, 2],
    [-1, 0, 1, 2],
])
def test_list_contains_tail_validation(value: List[Any]):
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_list_contains_tail_validation_incorrect_element_error():
    with given:
        value = [2]
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()[0], actual_value=value[0], expected_value=1),
            MissingElementValidationError(PathHolder(), actual_value=value, index=1),
        ]


def test_list_contains_tail_validation_missing_element_error():
    with given:
        value = [1]
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            MissingElementValidationError(PathHolder(), actual_value=value, index=1),
        ]


def test_list_contains_tail_validation_extra_element_error():
    with given:
        value = [1, 2, 3]
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()[1], actual_value=value[1], expected_value=1),
            ValueValidationError(PathHolder()[2], actual_value=value[2], expected_value=2),
        ]


def test_list_contains_validation_incorrect_tail_element_error():
    with given:
        value = [1, 3]
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()[1], actual_value=3, expected_value=2),
        ]


@pytest.mark.parametrize("value", [
    [1, 2],
    [1, 2, 3],
    [0, 1, 2],
    [0, 1, 2, 3],
])
def test_list_contains_body_validation(value: List[Any]):
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_list_contains_validation_incorrect_head_element_error():
    with given:
        value = [3, 2]
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()[0], actual_value=3, expected_value=1),
        ]


def test_list_contains_validation_extra_head_element_error():
    with given:
        value = [0, 1]
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            MissingElementValidationError(PathHolder(), actual_value=value, index=2)
        ]


def test_list_contains_validation_extra_tail_element_error():
    with given:
        value = [2, 3]
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()[0], actual_value=2, expected_value=1),
            ValueValidationError(PathHolder()[1], actual_value=3, expected_value=2),
        ]


def test_list_contains_validation_extra_body_element_error():
    with given:
        value = [1, 0, 2]
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()[1], actual_value=0, expected_value=2),
        ]


def test_list_contains_validation_missing_tail_element_error():
    with given:
        value = [1]
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            MissingElementValidationError(PathHolder(), actual_value=value, index=1),
        ]


def test_list_contains_validation_missing_head_element_error():
    with given:
        value = [2]
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()[0], actual_value=2, expected_value=1),
            MissingElementValidationError(PathHolder(), actual_value=value, index=1),
        ]


def test_list_contains_validation_incorrect_order_error():
    with given:
        value = [2, 1]
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            MissingElementValidationError(PathHolder(), actual_value=value, index=2),
        ]


def test_list_contains_validation_no_elements_error():
    with given:
        value = []
        sch = schema.list([..., schema.int, ...])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            MissingElementValidationError(PathHolder(), actual_value=value, index=0),
        ]

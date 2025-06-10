from typing import Any, List

import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import TypeValidationError, UniqueValidationError


@pytest.mark.parametrize("value", [
    [],
    [1, 2, 3],
    ["a", "b", "c"],
    [True, False],
])
def test_unique_list_validation(value: List[Any]):
    with when:
        result = validate(schema.list.unique(), value)

    with then:
        assert result.get_errors() == []


def test_unique_list_type_validation_error():
    with given:
        value = {}

    with when:
        result = validate(schema.list.unique(), value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), value, list),
        ]


def test_unique_list_with_duplicate_elements():
    with given:
        value = [1, 2, 1, 3]

    with when:
        result = validate(schema.list.unique(), value)

    with then:
        assert result.get_errors() == [
            UniqueValidationError(PathHolder(), value),
        ]


def test_unique_list_with_duplicate_strings():
    with given:
        value = ["a", "b", "a", "c"]

    with when:
        result = validate(schema.list.unique(), value)

    with then:
        assert result.get_errors() == [
            UniqueValidationError(PathHolder(), value),
        ]


def test_unique_list_with_duplicate_booleans():
    with given:
        value = [True, False, True]

    with when:
        result = validate(schema.list.unique(), value)

    with then:
        assert result.get_errors() == [
            UniqueValidationError(PathHolder(), value),
        ]


def test_unique_list_with_duplicate_mixed_types():
    with given:
        value = [1, "a", 1, True]

    with when:
        result = validate(schema.list.unique(), value)

    with then:
        assert result.get_errors() == [
            UniqueValidationError(PathHolder(), value),
        ]


def test_unique_list_with_typed_elements():
    with given:
        value = [1, 2, 3, 4, 5]

    with when:
        result = validate(schema.list(schema.int).unique(), value)

    with then:
        assert result.get_errors() == []


def test_unique_list_with_typed_duplicate_elements():
    with given:
        value = [1, 2, 3, 2, 5]

    with when:
        result = validate(schema.list(schema.int).unique(), value)

    with then:
        assert result.get_errors() == [
            UniqueValidationError(PathHolder(), value),
        ]


@pytest.mark.parametrize("value", [
    [],
    [1, 2, 3],
])
def test_unique_list_len_validation(value: List[Any]):
    with given:
        length = len(value)

    with when:
        result = validate(schema.list.len(length).unique(), value)

    with then:
        assert result.get_errors() == []


def test_unique_list_min_len_validation():
    with given:
        value = [1, 2, 3]
        min_length = 2

    with when:
        result = validate(schema.list.len(min_length, ...).unique(), value)

    with then:
        assert result.get_errors() == []


def test_unique_list_min_len_with_duplicates():
    with given:
        value = [1, 2, 2, 3]
        min_length = 2

    with when:
        result = validate(schema.list.len(min_length, ...).unique(), value)

    with then:
        assert result.get_errors() == [
            UniqueValidationError(PathHolder(), value),
        ]


def test_unique_list_max_len_validation():
    with given:
        value = [1, 2, 3]
        max_length = 5

    with when:
        result = validate(schema.list.len(..., max_length).unique(), value)

    with then:
        assert result.get_errors() == []


def test_unique_list_max_len_with_duplicates():
    with given:
        value = [1, 2, 2, 3]
        max_length = 5

    with when:
        result = validate(schema.list.len(..., max_length).unique(), value)

    with then:
        assert result.get_errors() == [
            UniqueValidationError(PathHolder(), value),
        ]


def test_unique_list_nested_lists():
    with given:
        value = [[1, 2], [3, 4], [5, 6]]

    with when:
        result = validate(schema.list(schema.list).unique(), value)

    with then:
        assert result.get_errors() == []


def test_unique_list_nested_lists_with_duplicates():
    with given:
        value = [[1, 2], [3, 4], [1, 2]]

    with when:
        result = validate(schema.list(schema.list).unique(), value)

    with then:
        assert result.get_errors() == [
            UniqueValidationError(PathHolder(), value),
        ]


def test_unique_list_with_none_values():
    with given:
        value = [None, 1, "a"]

    with when:
        result = validate(schema.list(schema.any(schema.none, schema.int, schema.str)).unique(),
                          value)

    with then:
        assert result.get_errors() == []


def test_unique_list_with_duplicate_none_values():
    with given:
        value = [None, 1, None]

    with when:
        result = validate(schema.list(schema.any(schema.none, schema.int)).unique(), value)

    with then:
        assert result.get_errors() == [
            UniqueValidationError(PathHolder(), value),
        ]


def test_unique_list_with_explicit_elements():
    with given:
        value = [1, 2, 3]

    with (when):
        result = \
            validate(schema.list([schema.int(1), schema.int(2), schema.int(3)]).unique(), value)

    with then:
        assert result.get_errors() == []

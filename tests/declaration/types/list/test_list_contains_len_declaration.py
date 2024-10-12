import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError


@pytest.mark.parametrize("length", [3, 4])
def test_list_contains_elements_len_declaration(length: int):
    with given:
        elements = [schema.int(1), schema.int(2), schema.int(3)]

    with when:
        sch = schema.list([..., *elements, ...]).len(length)

    with then:
        assert sch.props.elements == [..., *elements, ...]
        assert sch.props.len == length


def test_list_contains_elements_len_declaration_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        sch.len(1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` min len must be less than or equal to 2, 1 given"
        )


@pytest.mark.parametrize("min_length", [3, 2])
def test_list_contains_elements_min_len_declaration(min_length: int):
    with given:
        elements = [schema.int(1), schema.int(2), schema.int(3)]

    with when:
        sch = schema.list([..., *elements, ...]).len(min_length, ...)

    with then:
        assert sch.props.elements == [..., *elements, ...]
        assert sch.props.min_len == min_length


def test_list_contains_elements_min_len_declaration_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        sch.len(3, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` min len must be less than or equal to 2, 3 given"
        )


@pytest.mark.parametrize("max_length", [3, 4])
def test_list_contains_elements_max_len_declaration(max_length: int):
    with given:
        elements = [schema.int(1), schema.int(2), schema.int(3)]

    with when:
        sch = schema.list([..., *elements, ...]).len(..., max_length)

    with then:
        assert sch.props.elements == [..., *elements, ...]
        assert sch.props.max_len == max_length


def test_list_contains_elements_max_len_declaration_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        sch.len(..., 1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` max len must be greater than or equal to 2, 1 given"
        )


def test_list_contains_elements_min_max_len_declaration():
    with given:
        elements = [schema.int(1), schema.int(2), schema.int(3)]
        min_length, max_length = 3, 10

    with when:
        sch = schema.list([..., *elements, ...]).len(min_length, max_length)

    with then:
        assert sch.props.elements == [..., *elements, ...]
        assert sch.props.min_len == min_length
        assert sch.props.max_len == max_length


@pytest.mark.parametrize("length", [2, 3])
def test_list_contains_head_elements_len_declaration(length: int):
    with given:
        elements = [schema.int(1), schema.int(2)]

    with when:
        sch = schema.list([*elements, ...]).len(length)

    with then:
        assert sch.props.elements == [*elements, ...]
        assert sch.props.len == length


def test_list_contains_head_elements_len_declaration_error():
    with given:
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        sch.len(1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` min len must be less than or equal to 2, 1 given"
        )


@pytest.mark.parametrize("min_length", [2, 1])
def test_list_contains_head_elements_min_len_declaration(min_length: int):
    with given:
        elements = [schema.int(1), schema.int(2)]

    with when:
        sch = schema.list([*elements, ...]).len(min_length, ...)

    with then:
        assert sch.props.elements == [*elements, ...]
        assert sch.props.min_len == min_length


def test_list_contains_head_elements_min_len_declaration_error():
    with given:
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        sch.len(3, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` min len must be less than or equal to 2, 3 given"
        )


@pytest.mark.parametrize("max_length", [2, 3])
def test_list_contains_head_elements_max_len_declaration(max_length: int):
    with given:
        elements = [schema.int(1), schema.int(2)]

    with when:
        sch = schema.list([*elements, ...]).len(..., max_length)

    with then:
        assert sch.props.elements == [*elements, ...]
        assert sch.props.max_len == max_length


def test_list_contains_head_elements_max_len_declaration_error():
    with given:
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        sch.len(..., 1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` max len must be greater than or equal to 2, 1 given"
        )


def test_list_contains_head_elements_min_max_len_declaration():
    with given:
        elements = [schema.int(1), schema.int(2)]
        min_length, max_length = 2, 10

    with when:
        sch = schema.list([*elements, ...]).len(min_length, max_length)

    with then:
        assert sch.props.elements == [*elements, ...]
        assert sch.props.min_len == min_length
        assert sch.props.max_len == max_length


@pytest.mark.parametrize("length", [2, 3])
def test_list_contains_tail_elements_len_declaration(length: int):
    with given:
        elements = [schema.int(2), schema.int(3)]
        length = 2

    with when:
        sch = schema.list([..., *elements]).len(length)

    with then:
        assert sch.props.elements == [..., *elements]
        assert sch.props.len == length


def test_list_contains_tail_elements_len_declaration_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when, raises(Exception) as exception:
        sch.len(1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` min len must be less than or equal to 2, 1 given"
        )


@pytest.mark.parametrize("min_length", [2, 1])
def test_list_contains_tail_elements_min_len_declaration(min_length: int):
    with given:
        elements = [schema.int(2), schema.int(3)]

    with when:
        sch = schema.list([..., *elements]).len(min_length, ...)

    with then:
        assert sch.props.elements == [..., *elements]
        assert sch.props.min_len == min_length


def test_list_contains_tail_elements_min_len_declaration_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when, raises(Exception) as exception:
        sch.len(3, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` min len must be less than or equal to 2, 3 given"
        )


@pytest.mark.parametrize("max_length", [2, 3])
def test_list_contains_tail_elements_max_len_declaration(max_length: int):
    with given:
        elements = [schema.int(2), schema.int(3)]

    with when:
        sch = schema.list([..., *elements]).len(..., max_length)

    with then:
        assert sch.props.elements == [..., *elements]
        assert sch.props.max_len == max_length


def test_list_contains_tail_elements_max_len_declaration_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when, raises(Exception) as exception:
        sch.len(..., 1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` max len must be greater than or equal to 2, 1 given"
        )


def test_list_contains_tail_elements_min_max_len_declaration():
    with given:
        elements = [schema.int(2), schema.int(3)]
        min_length, max_length = 2, 10

    with when:
        sch = schema.list([..., *elements]).len(min_length, max_length)

    with then:
        assert sch.props.elements == [..., *elements]

from unittest.mock import sentinel

from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import ListSchema


def test_list_of_elements_declaration():
    with when:
        list_type = schema.int
        sch = schema.list(list_type)

    with then:
        assert isinstance(sch, ListSchema)
        assert sch.props.type == list_type


def test_list_of_invalid_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.list(sentinel)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.list` value must be an instance of ('list', 'Schema'), "
            "instance of '_Sentinel' given"
        )


def test_list_of_len_declaration():
    with given:
        list_type = schema.int
        length = 10

    with when:
        sch = schema.list(list_type).len(length)

    with then:
        assert sch.props.type == list_type
        assert sch.props.len == length


def test_list_of_min_len_declaration():
    with given:
        list_type = schema.int
        min_length = 10

    with when:
        sch = schema.list(list_type).len(min_length, ...)

    with then:
        assert sch.props.type == list_type
        assert sch.props.min_len == min_length


def test_list_of_max_len_declaration():
    with given:
        list_type = schema.int
        max_length = 10

    with when:
        sch = schema.list(list_type).len(..., max_length)

    with then:
        assert sch.props.type == list_type
        assert sch.props.max_len == max_length


def test_list_of_min_max_len_declaration():
    with given:
        list_type = schema.int
        min_length, max_length = 1, 10

    with when:
        sch = schema.list(list_type).len(min_length, max_length)

    with then:
        assert sch.props.type == list_type
        assert sch.props.min_len == min_length
        assert sch.props.max_len == max_length


def test_list_of_value_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(1)(schema.str)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(1)` is already declared"


def test_list_of_value_already_declared_min_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(1, ...)(schema.str)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(1, ...)` is already declared"


def test_list_of_value_already_declared_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(..., 1)(schema.str)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(..., 1)` is already declared"


def test_list_of_value_already_declared_min_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(1, 2)(schema.str)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(1, 2)` is already declared"

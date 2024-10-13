from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import ListSchema


def test_list_declaration():
    with when:
        sch = schema.list

    with then:
        assert isinstance(sch, ListSchema)


def test_list_empty_elements_declaration():
    with given:
        elements = []

    with when:
        sch = schema.list(elements)

    with then:
        assert sch.props.elements == elements


def test_list_elements_declaration():
    with given:
        elements = [schema.int(1), schema.int(2)]

    with when:
        sch = schema.list(elements)

    with then:
        assert sch.props.elements == elements


def test_list_invalid_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.list({})

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.list` value must be an instance of ('list', 'Schema'), "
            "instance of 'dict' given"
        )


def test_list_invalid_element_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.list(["banana"])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.list` value must be an instance of ('Schema', 'ellipsis'), "
            "instance of 'str' given"
        )


def test_list_already_declared_declaration_error():
    with when, raises(Exception) as exception:
        schema.list([])([])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list([])` is already declared"


def test_list_contains_any_elements_declaration():
    with when:
        sch = schema.list([...])

    with then:
        assert sch.props.elements == [...]


def test_list_contains_body_elements_declaration():
    with given:
        elements = [schema.int(1), schema.int(2), schema.int(3)]

    with when:
        sch = schema.list([..., *elements, ...])

    with then:
        assert sch.props.elements == [..., *elements, ...]


def test_list_contains_elements_body_twice_declaration():
    with when, raises(Exception) as exception:
        schema.list([..., ...])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`...` must be first or last element"


def test_list_contains_elements_middle_declaration_error():
    with when, raises(Exception) as exception:
        schema.list([schema.int(1), ..., schema.int(3)])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`...` must be first or last element"


def test_list_contains_head_elements_declaration():
    with given:
        elements = [schema.int(1), schema.int(2)]

    with when:
        sch = schema.list([*elements, ...])

    with then:
        assert sch.props.elements == [*elements, ...]


def test_list_contains_elements_head_twice_declaration_error():
    with when, raises(Exception) as exception:
        schema.list([..., ..., schema.int(3)])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`...` must be first or last element"


def test_list_contains_tail_elements_declaration():
    with given:
        elements = [schema.int(2), schema.int(3)]

    with when:
        sch = schema.list([..., *elements])

    with then:
        assert sch.props.elements == [..., *elements]


def test_list_contains_elements_tail_twice_declaration_error():
    with when, raises(Exception) as exception:
        schema.list([schema.int(1), ..., ...])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`...` must be first or last element"

import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError


def test_str_contains_declaration():
    with given:
        substr = "banana"

    with when:
        sch = schema.str.contains(substr)

    with then:
        assert sch.props.substr == substr


def test_str_invalid_substr_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.contains(42)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str` value must be an instance of 'str', "
                                        "instance of 'int' 42 given")


@pytest.mark.parametrize("substr", [
    "banana",
    "anan",
    "",
])
def test_str_contains_with_value_declaration(substr: str):
    with when:
        sch = schema.str("banana").contains(substr)

    with then:
        assert sch.props.substr == substr


def test_str_contains_already_declared_value_declaration_error():
    with given:
        sch = schema.str("banana!")

    with when, raises(Exception) as exception:
        sch.contains("yellow")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == f"`{sch!r}` does not contain 'yellow'"


def test_str_contains_already_declared_substr_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.contains("banana").contains("banana")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.contains('banana')` is already declared"


def test_str_value_already_declared_contains_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.contains("banana")("banana!")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.contains('banana')` is already declared"

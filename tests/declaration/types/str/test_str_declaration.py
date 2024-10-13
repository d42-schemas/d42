from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import StrSchema


def test_str_declaration():
    with when:
        sch = schema.str

    with then:
        assert isinstance(sch, StrSchema)


def test_str_value_declaration():
    with given:
        value = "banana"

    with when:
        sch = schema.str(value)

    with then:
        assert sch.props.value == value


def test_str_invalid_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.str(None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str` value must be an instance of 'str', "
                                        "instance of 'NoneType' None given")


def test_str_already_declared_declaration_error():
    with when, raises(Exception) as exception:
        schema.str("banana")("banana")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str('banana')` is already declared"

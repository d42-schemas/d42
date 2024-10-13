from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import BoolSchema


def test_bool_declaration():
    with when:
        sch = schema.bool

    with then:
        assert isinstance(sch, BoolSchema)


def test_bool_value_declaration():
    with given:
        value = True

    with when:
        sch = schema.bool(value)

    with then:
        assert sch.props.value == value


def test_bool_invalid_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.bool(1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.bool` value must be an instance of 'bool', "
                                        "instance of 'int' 1 given")


def test_bool_already_declared_declaration_error():
    with when, raises(Exception) as exception:
        schema.bool(True)(True)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bool(True)` is already declared"

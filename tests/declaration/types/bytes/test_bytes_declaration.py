from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import BytesSchema


def test_bytes_declaration():
    with when:
        sch = schema.bytes

    with then:
        assert isinstance(sch, BytesSchema)


def test_bytes_value_declaration():
    with given:
        value = b""

    with when:
        sch = schema.bytes(value)

    with then:
        assert sch.props.value == value


def test_bytes_invalid_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes("")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.bytes` value must be an instance of 'bytes', "
                                        "instance of 'str' '' given")


def test_bytes_already_declared_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes(b"")(b"")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes(b'')` is already declared"

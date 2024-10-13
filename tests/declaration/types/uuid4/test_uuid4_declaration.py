from uuid import uuid4

from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import UUID4Schema


def test_uuid4_declaration():
    with when:
        sch = schema.uuid4

    with then:
        assert isinstance(sch, UUID4Schema)


def test_uuid4_value_declaration():
    with given:
        value = uuid4()

    with when:
        sch = schema.uuid4(value)

    with then:
        assert sch.props.value == value


def test_uuid4_invalid_value_type_declaration_error():
    with given:
        value = str(uuid4())

    with when, raises(Exception) as exception:
        schema.uuid4(value)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.uuid4` value must be an instance of 'UUID', "
                                        f"instance of 'str' {value!r} given")


def test_uuid4_already_declared_declaration_error():
    with given:
        value = uuid4()
        another_value = uuid4()

    with when, raises(Exception) as exception:
        schema.uuid4(value)(another_value)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == f"`schema.uuid4({value!r})` is already declared"

from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration.errors import DeclarationError
from d42.declaration.types import AnySchema


def test_any_declaration():
    with when:
        sch = schema.any

    with then:
        assert isinstance(sch, AnySchema)


def test_any_without_types_declaration_error():
    with when, raises(Exception) as exception:
        schema.any()

    with then:
        assert exception.type is TypeError
        assert "missing 1 required positional argument: 'type_'" in str(exception.value)


def test_any_type_declaration():
    with given:
        type_ = schema.none

    with when:
        sch = schema.any(type_)

    with then:
        assert sch.props.types == (type_,)


def test_any_non_schema_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.any(None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.any` value must be an instance of 'Schema', "
                                        "instance of 'NoneType' None given")


def test_any_types_already_declared_declaration_error():
    with when, raises(Exception) as exception:
        schema.any(schema.none)(schema.none)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.any(schema.none)` is already declared"


def test_any_types_declaration():
    with given:
        types = (schema.int, schema.str,)

    with when:
        sch = schema.any(*types)

    with then:
        assert sch.props.types == types


def test_any_types_with_values_declaration():
    with given:
        types = (schema.int(42), schema.str("banana"),)

    with when:
        sch = schema.any(*types)

    with then:
        assert sch.props.types == types

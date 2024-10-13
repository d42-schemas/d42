from baby_steps import given, then, when
from niltype import Nil
from pytest import raises

from d42 import schema
from d42.declaration import GenericSchema
from d42.declaration.types import (
    AnySchema,
    GenericTypeAliasSchema,
    StrSchema,
    TypeAliasProps,
    TypeAliasSchema,
)


def test_alias_declaration():
    with given:
        name = "uint_schema"
        sch = schema.int.min(0)

    with when:
        alias = schema.alias(name, sch)

    with then:
        assert isinstance(alias, TypeAliasSchema)
        assert alias.props.type == sch
        assert alias.props.name == name


def test_alias_declaration_error():
    with when, raises(Exception) as exception:
        schema.alias()

    with then:
        assert exception.type is TypeError


def test_alias_default_declaration():
    with when:
        sch = TypeAliasSchema()

    with then:
        assert isinstance(sch.props.type, AnySchema)
        assert sch.props.name is Nil


def test_alias_custom_declaration():
    with then:
        class AliasSchema(GenericTypeAliasSchema[TypeAliasProps]):
            pass

    with when:
        sch = AliasSchema()

    with then:
        assert isinstance(sch.props.type, AnySchema)
        assert sch.props.name is Nil


def test_alias_custom_type_declaration():
    with then:
        class AliasProps(TypeAliasProps):
            @property
            def type(self) -> GenericSchema:
                return self.get("type", StrSchema())

        class AliasSchema(GenericTypeAliasSchema[AliasProps]):
            pass

    with when:
        sch = AliasSchema()

    with then:
        assert isinstance(sch.props.type, StrSchema)
        assert sch.props.name is Nil

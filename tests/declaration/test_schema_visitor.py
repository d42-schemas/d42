import pytest
from baby_steps import given, then, when
from pytest import raises

from d42.declaration import GenericSchema, SchemaVisitor
from d42.declaration.types import (
    AnySchema,
    BoolSchema,
    BytesSchema,
    DateTimeSchema,
    DictSchema,
    FloatSchema,
    IntSchema,
    ListSchema,
    NoneSchema,
    StrSchema,
    TypeAliasSchema,
    UUID4Schema,
)


@pytest.mark.parametrize(("method", "schema"), [
    ("visit_none", NoneSchema()),
    ("visit_bool", BoolSchema()),
    ("visit_int", IntSchema()),
    ("visit_float", FloatSchema()),
    ("visit_str", StrSchema()),
    ("visit_list", ListSchema()),
    ("visit_dict", DictSchema()),
    ("visit_any", AnySchema()),
    ("visit_bytes", BytesSchema()),
    ("visit_uuid4", UUID4Schema()),
    ("visit_datetime", DateTimeSchema()),
])
def test_schema_visitor_visit_type(method: str, schema: GenericSchema):
    with given:
        visitor = SchemaVisitor()

    with when, raises(Exception) as exception:
        getattr(visitor, method)(schema)

    with then:
        assert exception.type is NotImplementedError


def test_schema_visitor_visit_type_alias():
    with given:
        visitor = SchemaVisitor()
        schema = TypeAliasSchema()

    with when, raises(Exception) as exception:
        visitor.visit_type_alias(schema)

    with then:
        assert exception.type is NotImplementedError


def test_schema_get_attr():
    with given:
        visitor = SchemaVisitor()

    with when, raises(AttributeError) as exception:
        visitor.unknown

    with then:
        assert exception.type is AttributeError
        assert str(exception.value) == "'SchemaVisitor' object has no attribute 'unknown'"

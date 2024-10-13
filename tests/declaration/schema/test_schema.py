from unittest.mock import sentinel

from baby_steps import given, then, when
from pytest import raises

from d42.declaration import Props, Schema, SchemaVisitor


def test_schema_abc():
    with when, raises(Exception) as exception:
        Schema()

    with then:
        assert exception.type is TypeError
        assert str(exception.value) == "Cannot instantiate abstract class Schema"


def test_schema_accept_visitor():
    with given:
        class CustomType(Schema[Props]):
            pass

        class CustomVisitor(SchemaVisitor):
            def visit(self, schema, **kwargs):
                return sentinel.visited

        custom_type = CustomType()
        custom_visitor = CustomVisitor()

    with when:
        res = custom_type.__accept__(custom_visitor)

    with then:
        assert res is sentinel.visited


def test_schema_accept_visitor_without_visit():
    with given:
        class CustomType(Schema[Props]):
            pass

        class CustomVisitor(SchemaVisitor):
            pass

        custom_type = CustomType()
        custom_visitor = CustomVisitor()

    with when, raises(Exception) as exception:
        custom_type.__accept__(custom_visitor)

    with then:
        assert exception.type is NotImplementedError
        assert str(exception.value) == "CustomVisitor has no method 'visit'"

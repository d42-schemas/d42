from baby_steps import given, then, when
from pytest import raises

from d42.declaration import Props, Schema
from d42.representation import Representor, represent


def test_register_visitor():
    with given:
        representation = "schema.custom_type"

        class CustomType(Schema[Props]):
            def __accept__(self, visitor, **kwargs):
                return visitor.visit_custom_type(self, **kwargs)

        class CustomRepresentor(Representor, extend=True):
            def visit_custom_type(self, schema, **kwargs):
                return representation

    with when:
        res = represent(CustomType())

    with then:
        assert res == representation


def test_register_visitor_without_extend():
    with given:
        class AnotherCustomType(Schema[Props]):
            def __accept__(self, visitor, **kwargs):
                return visitor.visit_another_custom_type(self, **kwargs)

        class CustomRepresentor(Representor):
            def visit_another_custom_type(self, schema, **kwargs):
                return "schema.another_custom_type"

    with when, raises(Exception) as exception:
        represent(AnotherCustomType())

    with then:
        assert exception.type is AttributeError

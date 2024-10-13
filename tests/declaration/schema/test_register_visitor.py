from baby_steps import given, then, when

from d42.declaration import Props, Schema, SchemaVisitor


def test_register_visitor():
    with given:
        representation = "schema.custom_type"

        class CustomType(Schema[Props]):
            def __accept__(self, visitor, **kwargs):
                return visitor.visit_custom_type(self, **kwargs)

        class CustomRepresentor(SchemaVisitor, extend=True):
            def visit_custom_type(self, schema, **kwargs):
                return representation

    with when:
        res = CustomType().__accept__(CustomRepresentor())

    with then:
        assert res == representation

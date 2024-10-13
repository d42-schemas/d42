from baby_steps import then, when

from d42 import schema
from d42.declaration import union


def test_union():
    with when:
        res = union(schema.str, schema.none)

    with then:
        assert res == schema.any(schema.str, schema.none)


def test_union_nested():
    with when:
        res = union(union(schema.str, schema.int), schema.none)

    with then:
        assert res == schema.any(schema.any(schema.str, schema.int), schema.none)

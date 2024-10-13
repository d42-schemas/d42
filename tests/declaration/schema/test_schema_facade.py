from baby_steps import then, when

from d42 import schema


def test_schema_eq():
    with when:
        res = (schema.int == schema.int)

    with then:
        assert res is True


def test_schema_not_eq():
    with when:
        res = (schema.int == schema.str)

    with then:
        assert res is False


def test_schema_ne():
    with when:
        res = (schema.int != schema.str)

    with then:
        assert res is True


def test_schema_not_ne():
    with when:
        res = (schema.int != schema.int)

    with then:
        assert res is False

from baby_steps import then, when
from pytest import raises

from d42 import schema
from d42.declaration.types import NoneSchema


def test_none_declaration():
    with when:
        sch = schema.none

    with then:
        assert isinstance(sch, NoneSchema)


def test_none_value_declaration_error():
    with when, raises(Exception) as exception:
        schema.none(None)

    with then:
        assert exception.type is TypeError
        assert str(exception.value) == "'NoneSchema' object is not callable"

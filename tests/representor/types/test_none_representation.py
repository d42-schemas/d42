from baby_steps import given, then, when

from d42 import schema
from d42.representation import represent


def test_none_representation():
    with given:
        sch = schema.none

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.none"

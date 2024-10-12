from datetime import datetime

from baby_steps import given, then, when

from d42 import schema
from d42.representor import represent


def test_datetime_representation():
    with given:
        sch = schema.datetime

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.datetime"


def test_datetime_value_representation():
    with given:
        dt = datetime.now()
        sch = schema.datetime(dt)

    with when:
        res = represent(sch)

    with then:
        assert res == f"schema.datetime({dt!r})"

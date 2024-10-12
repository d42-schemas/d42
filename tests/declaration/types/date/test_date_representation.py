from datetime import date

from baby_steps import given, then, when

from d42 import schema
from d42.representor import represent


def test_date_representation():
    with given:
        sch = schema.date

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.date"


def test_date_value_representation():
    with given:
        dt = date.today()
        sch = schema.date(dt)

    with when:
        res = represent(sch)

    with then:
        assert res == f"schema.date({dt!r})"

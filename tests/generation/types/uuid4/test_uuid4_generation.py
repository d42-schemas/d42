from uuid import UUID, uuid4

from baby_steps import given, then, when

from d42 import fake, schema


def test_uuid4_generation():
    with given:
        sch = schema.uuid4

    with when:
        res = fake(sch)

    with then:
        assert isinstance(res, UUID)


def test_uuid4_value_generation():
    with given:
        val = uuid4()
        sch = schema.uuid4(val)

    with when:
        res = fake(sch)

    with then:
        assert res == val

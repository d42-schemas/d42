from baby_steps import given, then, when
from pytest import raises

from d42 import optional, schema


def test_dict_add():
    with given:
        sch1 = schema.dict({"id": schema.int})
        sch2 = schema.dict({"name": schema.str})

    with when:
        res = sch1 + sch2

    with then:
        assert res == schema.dict({
            "id": schema.int,
            "name": schema.str
        })
        assert sch1 == schema.dict({"id": schema.int})
        assert sch2 == schema.dict({"name": schema.str})


def test_dict_add_overide():
    with given:
        sch1 = schema.dict({"id": schema.int})
        sch2 = schema.dict({"id": schema.str})

    with when:
        res = sch1 + sch2

    with then:
        assert res == schema.dict({
            "id": schema.str
        })
        assert sch1 == schema.dict({"id": schema.int})
        assert sch2 == schema.dict({"id": schema.str})


def test_dict_add_optional():
    with given:
        sch1 = schema.dict({"id": schema.int})
        sch2 = schema.dict({"name": schema.str, optional("created_at"): schema.int})

    with when:
        res = sch1 + sch2

    with then:
        assert res == schema.dict({
            "id": schema.int,
            "name": schema.str,
            optional("created_at"): schema.int
        })
        assert sch1 == schema.dict({"id": schema.int})
        assert sch2 == schema.dict({"name": schema.str, optional("created_at"): schema.int})


def test_dict_add_optional_override():
    with given:
        sch1 = schema.dict({"id": schema.int, optional("created_at"): schema.int})
        sch2 = schema.dict({"name": schema.str, "created_at": schema.int})

    with when:
        res = sch1 + sch2

    with then:
        assert res == schema.dict({
            "id": schema.int,
            "name": schema.str,
            "created_at": schema.int
        })
        assert sch1 == schema.dict({"id": schema.int, optional("created_at"): schema.int})
        assert sch2 == schema.dict({"name": schema.str, "created_at": schema.int})


def test_dict_add_relaxed_left():
    with given:
        sch1 = schema.dict({"id": schema.int, ...: ...})
        sch2 = schema.dict({"name": schema.str})

    with when:
        res = sch1 + sch2

    with then:
        assert res == schema.dict({
            "id": schema.int,
            ...: ...,
            "name": schema.str
        })
        assert sch1 == schema.dict({"id": schema.int, ...: ...})
        assert sch2 == schema.dict({"name": schema.str})


def test_dict_add_relaxed_right():
    with given:
        sch1 = schema.dict({"id": schema.int})
        sch2 = schema.dict({"name": schema.str, ...: ...})

    with when:
        res = sch1 + sch2

    with then:
        assert res == schema.dict({
            "id": schema.int,
            "name": schema.str,
            ...: ...,
        })
        assert sch1 == schema.dict({"id": schema.int})
        assert sch2 == schema.dict({"name": schema.str, ...: ...})


def test_dict_add_incorrect_type():
    with given:
        sch = schema.dict

    with when, raises(Exception) as exception:
        sch + {}

    with then:
        assert exception.type is TypeError
        assert str(exception.value) == (
            "Unsupported operand type for +: 'DictSchema' and <class 'dict'>"
        )

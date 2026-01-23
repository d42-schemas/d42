from baby_steps import given, then, when

from d42 import optional, schema
from d42.substitution import substitute


def test_dict_optional_absent_substitution():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("deleted_at"): schema.int
        })

    with when:
        res = substitute(sch, {
            "id": 1,
            "deleted_at": optional.absent
        })

    with then:
        assert "deleted_at" not in res.keys()
        assert res.props.absent_keys == {"deleted_at"}


def test_dict_multiple_optional_absent_substitution():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("created_at"): schema.int,
            optional("deleted_at"): schema.int
        })

    with when:
        res = substitute(sch, {
            "id": 1,
            "deleted_at": optional.absent,
            "created_at": optional.absent
        })

    with then:
        assert "deleted_at" not in res.keys()
        assert "created_at" not in res.keys()
        assert res.props.absent_keys == {"deleted_at", "created_at"}


def test_dict_nested_optional_absent_substitution():
    with given:
        sch = schema.dict({
            "users": schema.list(schema.dict({
                "id": schema.int,
                optional("deleted_at"): schema.int
            }))
        })

    with when:
        res = substitute(sch, {
            "users": [
                {
                    "id": 1,
                    "deleted_at": optional.absent
                }
            ]
        })

    with then:
        user_schema = res.props.keys["users"][0].props.elements[0]
        assert "deleted_at" not in user_schema.keys()
        assert user_schema.props.absent_keys == {"deleted_at"}


def test_dict_optional_present_substitution():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str
        })

    with when:
        res = substitute(sch, {
            "id": 1,
            "name": optional.present
        })

    with then:
        assert res == schema.dict({
            "id": schema.int(1),
            "name": schema.str,
        })
        assert res != sch


def test_dict_multiple_optional_present_substitution():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str,
            optional("email"): schema.str
        })

    with when:
        res = substitute(sch, {
            "id": 1,
            "name": optional.present,
            "email": optional.present
        })

    with then:
        assert res == schema.dict({
            "id": schema.int(1),
            "name": schema.str,
            "email": schema.str,
        })
        assert res != sch


def test_dict_nested_optional_present_substitution():
    with given:
        sch = schema.dict({
            "users": schema.list(schema.dict({
                "id": schema.int,
                optional("name"): schema.str
            }))
        })

    with when:
        res = substitute(sch, {
            "users": [
                {
                    "id": 1,
                    "name": optional.present
                }
            ]
        })

    with then:
        assert res == schema.dict({
            "users": schema.list([
                schema.dict({
                    "id": schema.int(1),
                    "name": schema.str,
                })
            ])
        })
        assert res != sch

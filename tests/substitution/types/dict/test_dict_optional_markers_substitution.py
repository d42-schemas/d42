from baby_steps import given, then, when
from pytest import raises

from d42 import optional, schema
from d42.declaration.types import is_absent
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError


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
        assert set(res.keys()) == {"id"}
        assert is_absent(res.props.keys["deleted_at"][1])
        assert res != sch


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
        assert set(res.keys()) == {"id"}
        assert is_absent(res.props.keys["deleted_at"][1])
        assert is_absent(res.props.keys["created_at"][1])
        assert res != sch


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
        assert set(user_schema.keys()) == {"id"}
        assert is_absent(user_schema.props.keys["deleted_at"][1])
        assert res != sch


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


def test_dict_required_key_optional_absent_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
        })

    with when, raises(Exception) as exception:
        substitute(sch, {
            "id": optional.absent,
        })

    with then:
        assert exception.type is SubstitutionError


def test_dict_required_key_optional_present_is_noop():
    with given:
        sch = schema.dict({
            "id": schema.int,
        })

    with when:
        res = substitute(sch, {
            "id": optional.present,
        })

    with then:
        assert res == schema.dict({
            "id": schema.int,
        })

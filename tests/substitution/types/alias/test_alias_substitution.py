from baby_steps import given, then, when
from niltype import Nil
from pytest import raises

from d42 import schema
from d42.declaration.types import TypeAliasSchema
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError


def test_alias_default_substitution():
    with given:
        sch = TypeAliasSchema()

    with when:
        res = substitute(sch, None)

    with then:
        assert res.props.type == schema.any(schema.none)
        assert res.props.name is Nil
        assert res != sch


def test_alias_substitution():
    with given:
        name = "uint"
        sch = schema.alias(name, schema.int.min(0))

    with when:
        res = substitute(sch, 42)

    with then:
        assert res.props.type == schema.int(42).min(0)
        assert res.props.name == name
        assert res != sch


def test_alias_substitution_error():
    with given:
        sch = schema.alias("uint", schema.int.min(0))

    with when, raises(Exception) as exception:
        substitute(sch, -1)

    with then:
        assert exception.type is SubstitutionError

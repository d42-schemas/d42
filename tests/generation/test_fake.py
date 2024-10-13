from baby_steps import then, when
from pytest import raises

from d42 import fake, schema


def test_fake():
    with when:
        res = fake(schema.int)

    with then:
        isinstance(res, int)


def test_fake_incorrect_type():
    with when, raises(Exception) as exception:
        fake(object)

    with then:
        assert exception.type is TypeError
        assert str(exception.value) == (
            "Expected 'schema' to be an instance of 'district42.types.Schema', "
            "got <class 'object'> instead"
        )

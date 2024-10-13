from unittest.mock import Mock, call, sentinel

from baby_steps import given, then, when
from pytest import raises

from d42.declaration import Props, Schema
from d42.substitution import Substitutor
from d42.validation import Formatter, Validator


def test_substitutor_validator():
    with given:
        substitutor = Substitutor()

    with when:
        res = substitutor.validator

    with then:
        assert isinstance(res, Validator)


def test_substitutor_formatter():
    with given:
        substitutor = Substitutor()

    with when:
        res = substitutor.formatter

    with then:
        assert isinstance(res, Formatter)


def test_substitutor_visit():
    with given:
        mock = Mock(return_value=sentinel.visited)

        class CustomType(Schema[Props]):
            def __d42_substitute__(self, *args, **kwargs) -> str:
                return mock(*args, **kwargs)

        custom_type = CustomType()
        substitutor = Substitutor()

    with when:
        res = substitutor.visit(custom_type, value=sentinel.value)

    with then:
        assert res is sentinel.visited
        assert mock.mock_calls == [
            call(substitutor, value=sentinel.value)
        ]


def test_substitutor_visit_error():
    with given:
        class CustomType(Schema[Props]):
            pass

        custom_type = CustomType()
        substitutor = Substitutor()

    with when, raises(Exception) as exception:
        substitutor.visit(custom_type)

    with then:
        assert exception.type is NotImplementedError
        assert str(exception.value) == "CustomType has no method '__d42_substitute__'"

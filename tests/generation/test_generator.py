from unittest.mock import Mock, call, sentinel

from baby_steps import given, then, when
from pytest import raises

from d42.declaration import Props, Schema
from d42.generation import Generator, Random

from ._fixtures import generator, random_, regex_generator

__all__ = ("generator", "random_", "regex_generator",)  # noqa: F401


def test_generator_random(generator: Generator):
    with when:
        res = generator.random

    with then:
        assert isinstance(res, Random)


def test_generator_visit(generator: Generator):
    with given:
        mock = Mock(return_value=sentinel.visited)

        class CustomType(Schema[Props]):
            def __d42_generate__(self, *args, **kwargs) -> str:
                return mock(*args, **kwargs)

        custom_type = CustomType()

    with when:
        res = generator.visit(custom_type)

    with then:
        assert res is sentinel.visited
        assert mock.mock_calls == [
            call(generator)
        ]


def test_generator_visit_error(generator: Generator):
    with given:
        class CustomType(Schema[Props]):
            pass

        custom_type = CustomType()

    with when, raises(Exception) as exception:
        generator.visit(custom_type)

    with then:
        assert exception.type is NotImplementedError
        assert str(exception.value) == "CustomType has no method '__d42_generate__'"

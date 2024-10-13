from unittest.mock import Mock, call, sentinel

from baby_steps import given, then, when
from pytest import raises

from d42.custom_type import CustomSchema, Props
from d42.custom_type.visitors import Generator, Representor, Substitutor, Validator
from d42.generation import Random, RegexGenerator


def test_custom_type_abc():
    with when, raises(Exception) as exception:
        CustomSchema()

    with then:
        assert exception.type is TypeError
        assert str(exception.value) == "Cannot instantiate abstract class CustomSchema"


def test_custom_type():
    with given:
        class CustomType(CustomSchema[Props]):
            pass

    with when:
        custom_type = CustomType()

    with then:
        assert isinstance(custom_type, CustomSchema)


def test_custom_type_represent():
    with given:
        mock = Mock(return_value=sentinel.visited)

        class CustomType(CustomSchema[Props]):
            __d42_represent__ = mock

        representor = Representor()
        custom_type = CustomType()

    with when:
        res = representor.visit(custom_type)

    with then:
        assert res is sentinel.visited
        assert mock.mock_calls == [
            call(representor, indent=0)
        ]


def test_custom_type_represent_default():
    with given:
        class CustomType(CustomSchema[Props]):
            pass

        representor = Representor()
        custom_type = CustomType()

    with when:
        res = representor.visit(custom_type)

    with then:
        assert res == "<CustomType>"


def test_custom_type_generate():
    with given:
        mock = Mock(return_value=sentinel.visited)

        class CustomType(CustomSchema[Props]):
            __d42_generate__ = mock

        random = Random()
        generator = Generator(random, RegexGenerator(random))
        custom_type = CustomType()

    with when:
        res = generator.visit(custom_type)

    with then:
        assert res is sentinel.visited
        assert mock.mock_calls == [
            call(generator)
        ]


def test_custom_type_generate_error():
    with given:
        class CustomType(CustomSchema[Props]):
            pass

        random = Random()
        generator = Generator(random, RegexGenerator(random))
        custom_type = CustomType()

    with when, raises(Exception) as exception:
        generator.visit(custom_type)

    with then:
        assert exception.type is NotImplementedError
        assert str(exception.value) == "CustomType has no method '__generate__'"


def test_custom_type_validate():
    with given:
        mock = Mock(return_value=sentinel.visited)

        class CustomType(CustomSchema[Props]):
            __d42_validate__ = mock

        validator = Validator()
        custom_type = CustomType()

    with when:
        res = validator.visit(custom_type, value=sentinel.value, path=sentinel.path)

    with then:
        assert res is sentinel.visited
        assert mock.mock_calls == [
            call(validator, value=sentinel.value, path=sentinel.path)
        ]


def test_custom_type_validate_error():
    with given:
        class CustomType(CustomSchema[Props]):
            pass

        validator = Validator()
        custom_type = CustomType()

    with when, raises(Exception) as exception:
        validator.visit(custom_type, value=sentinel.value, path=sentinel.path)

    with then:
        assert exception.type is NotImplementedError
        assert str(exception.value) == "CustomType has no method '__validate__'"


def test_custom_type_substitute():
    with given:
        mock = Mock(return_value=sentinel.visited)

        class CustomType(CustomSchema[Props]):
            __d42_substitute__ = mock

        substitutor = Substitutor()
        custom_type = CustomType()

    with when:
        res = substitutor.visit(custom_type, value=sentinel.value)

    with then:
        assert res is sentinel.visited
        assert mock.mock_calls == [
            call(substitutor, value=sentinel.value)
        ]


def test_custom_type_substitute_error():
    with given:
        class CustomType(CustomSchema[Props]):
            pass

        substitutor = Substitutor()
        custom_type = CustomType()

    with when, raises(Exception) as exception:
        substitutor.visit(custom_type, value=sentinel.value)

    with then:
        assert exception.type is NotImplementedError
        assert str(exception.value) == "CustomType has no method '__substitute__'"

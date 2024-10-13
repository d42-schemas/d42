from unittest.mock import Mock, call, sentinel

from baby_steps import given, then, when
from pytest import raises
from th import PathHolder

from d42.declaration import Props, Schema
from d42.validation import ValidationResult, Validator


def test_validator_path_holder_factory():
    with given:
        validator = Validator()

    with when:
        path = validator.make_path()

    with then:
        assert isinstance(path, PathHolder)


def test_validator_validation_result_factory():
    with given:
        validator = Validator()

    with when:
        path = validator.make_validation_result()

    with then:
        assert isinstance(path, ValidationResult)


def test_validator_visit():
    with given:
        mock = Mock(return_value=sentinel.visited)

        class CustomType(Schema[Props]):
            def __d42_validate__(self, *args, **kwargs) -> str:
                return mock(*args, **kwargs)

        custom_type = CustomType()
        validator = Validator()

    with when:
        res = validator.visit(custom_type, value=sentinel.value, path=sentinel.path)

    with then:
        assert res is sentinel.visited
        assert mock.mock_calls == [
            call(validator, value=sentinel.value, path=sentinel.path)
        ]


def test_validator_visit_error():
    with given:
        class CustomType(Schema[Props]):
            pass

        custom_type = CustomType()
        validator = Validator()

    with when, raises(Exception) as exception:
        validator.visit(custom_type)

    with then:
        assert exception.type is NotImplementedError
        assert str(exception.value) == "CustomType has no method '__d42_validate__'"

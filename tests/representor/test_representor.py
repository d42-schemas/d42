from unittest.mock import Mock, call, sentinel

from baby_steps import given, then, when
from pytest import raises

from d42.declaration import Props, Schema
from d42.representation import Representor


def test_representor_name():
    with given:
        representor = Representor()

    with when:
        res = representor.name

    with then:
        assert res == "schema"


def test_representor_visit():
    with given:
        mock = Mock(return_value=sentinel.visited)

        class CustomType(Schema[Props]):
            def __d42_represent__(self, *args, **kwargs) -> str:
                return mock(*args, **kwargs)

        custom_type = CustomType()
        representor = Representor()

    with when:
        res = representor.visit(custom_type)

    with then:
        assert res is sentinel.visited
        assert mock.mock_calls == [
            call(representor, indent=0)
        ]


def test_representor_visit_error():
    with given:
        class CustomType(Schema[Props]):
            pass

        custom_type = CustomType()
        representor = Representor()

    with when, raises(Exception) as exception:
        representor.visit(custom_type)

    with then:
        assert exception.type is NotImplementedError
        assert str(exception.value) == "CustomType has no method '__d42_represent__'"

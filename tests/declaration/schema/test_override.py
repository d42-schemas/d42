from unittest.mock import Mock, call

import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import Schema


def test_non_implemented_mod():
    with when, raises(Exception) as exception:
        schema.str.__mod__(None)

    with then:
        assert exception.type is AttributeError


@pytest.mark.parametrize("method", [
    "__invert__",
    "__mod__",
    "__add__",
])
def test_override_invert(method):
    with given:
        mock_ = Mock()
        Schema.__override__(method, mock_)

    with when:
        getattr(schema.str, method)()

    with then:
        assert mock_.mock_calls == [call()]

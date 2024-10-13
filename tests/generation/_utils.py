from unittest.mock import DEFAULT, Mock

from d42.declaration import Schema

__all__ = ("schema_mock",)


def schema_mock(return_value=DEFAULT):
    return Mock(Schema, __accept__=Mock(return_value=return_value))

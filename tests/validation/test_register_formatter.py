from baby_steps import given, then, when
from pytest import raises

from d42.validation import Formatter
from d42.validation.errors import ValidationError


def test_register_formatter():
    with given:
        formatted = "<custom_error>"

        class CustomError(ValidationError):
            def format(self, formatter: Formatter) -> str:
                return formatter.format_custom_error(self)

        class CustomFormatter(Formatter, extend=True):
            def format_custom_error(self, error: CustomError) -> str:
                return formatted

    with when:
        res = CustomError().format(CustomFormatter())

    with then:
        assert res == formatted


def test_register_formatter_without_extend():
    with given:
        formatted = "<another_custom_error>"

        class AnotherCustomError(ValidationError):
            def format(self, formatter: Formatter) -> str:
                return formatter.format_another_custom_error(self)

        class AnotherCustomFormatter(Formatter):
            def format_custom_error(self, error: AnotherCustomError) -> str:
                return formatted

    with when, raises(Exception) as exception:
        AnotherCustomError().format(AnotherCustomFormatter())

    with then:
        assert exception.type is AttributeError

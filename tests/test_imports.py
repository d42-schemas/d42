def test_district42():
    from d42 import from_native, make_required, optional, register_type, schema  # noqa


def test_blahblah():
    from d42 import fake  # noqa


def test_valera():
    from d42 import ValidationException, validate, validate_or_fail  # noqa


def test_revolt():
    from d42 import schema
    assert schema.str % "revolt" == schema.str("revolt")


def test_custom_type():
    from d42.custom_type import (  # noqa
        CustomSchema,
        Formatter,
        PathHolder,
        Props,
        PropsType,
        Schema,
        ValidationResult,
        register_type,
    )


def test_custom_type_visitors():
    from d42.custom_type.visitors import Generator, Representor, Substitutor, Validator  # noqa


def test_custom_type_errors():
    from d42.custom_type.errors import (  # noqa
        DeclarationError,
        SubstitutionError,
        TypeValidationError,
        ValidationError,
        ValueValidationError,
    )


def test_custom_type_utils():
    from d42.custom_type.utils import (  # noqa
        make_already_declared_error,
        make_invalid_type_error,
        make_substitution_error,
    )

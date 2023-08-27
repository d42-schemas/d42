import unittest


class TestImports(unittest.TestCase):
    def test_district42(self):
        from d42 import from_native, make_required, optional, register_type, schema  # noqa

    def test_blahblah(self):
        from d42 import fake  # noqa

    def test_valera(self):
        from d42 import ValidationException, validate, validate_or_fail  # noqa

    def test_revolt(self):
        from d42 import schema
        assert schema.str % "revolt" == schema.str("revolt")

    def test_custom_type(self):
        from d42.custom_type import (  # noqa
            CustomSchema,
            Formatter,
            PathHolder,
            Props,
            PropsType,
            Schema,
            ValidationResult,
        )

    def test_custom_type_visitors(self):
        from d42.custom_type.visitors import Generator, Representor, Substitutor, Validator  # noqa

    def test_custom_type_errors(self):
        from d42.custom_type.errors import (  # noqa
            DeclarationError,
            SubstitutionError,
            ValidationError,
        )

    def test_custom_type_utils(self):
        from d42.custom_type.utils import make_substitution_error, register_type  # noqa

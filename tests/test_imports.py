import unittest


class TestImports(unittest.TestCase):
    def test_district42(self):
        from d42 import from_native, optional, register_type, schema  # noqa

    def test_blahblah(self):
        from d42 import fake  # noqa

    def test_valera(self):
        from d42 import validate, validate_or_fail  # noqa

    def test_revolt(self):
        from d42 import schema
        assert schema.str % "revolt" == schema.str("revolt")

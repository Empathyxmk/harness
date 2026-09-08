from django import test
from django_google_maps.fields import typename


class TypeNamePublicTests(test.TestCase):
    def test_simple_type_returns_type_name_as_string_public(self):
        self.assertEqual('str', typename("abc"))

    def test_class_object_public(self):
        class Y:
            pass

        self.assertEqual('type', typename(Y))
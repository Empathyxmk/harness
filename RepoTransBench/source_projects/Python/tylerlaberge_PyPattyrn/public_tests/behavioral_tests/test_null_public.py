from unittest import TestCase
from pypattyrn.behavioral.null import Null

class NullPatternPublicTestCase(TestCase):
    def test_null_str_public(self):
        n = Null()
        self.assertEqual(str(n), "Null()")

    def test_attribute_get_set_public(self):
        n = Null()
        n.some_attr = 42
        self.assertEqual(n.some_attr, n)
        self.assertIsInstance(n, Null)
        self.assertIsNone(n())

    def test_eq_hash_public(self):
        a = Null()
        b = Null()
        self.assertEqual(a, b)
        self.assertTrue(hash(a) == hash(b))
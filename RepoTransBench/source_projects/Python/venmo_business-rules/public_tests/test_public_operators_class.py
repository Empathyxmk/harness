from business_rules.operators import BaseType, StringType, NumericType, BooleanType
from unittest import TestCase

class PublicOperatorsClassTestCase(TestCase):

    def test_base_type_value_public(self):
        base = BaseType('Value1')
        self.assertEqual(base.value, 'Value1')

    def test_string_type_inheritance_public(self):
        s = StringType('PublicString')
        self.assertIsInstance(s, BaseType)
        self.assertEqual(s.value, 'PublicString')

    def test_numeric_type_inheritance_public(self):
        n = NumericType(999)
        self.assertIsInstance(n, BaseType)
        self.assertEqual(n.value, 999)

    def test_boolean_type_inheritance_public(self):
        b = BooleanType(True)
        self.assertIsInstance(b, BaseType)
        self.assertEqual(b.value, True)
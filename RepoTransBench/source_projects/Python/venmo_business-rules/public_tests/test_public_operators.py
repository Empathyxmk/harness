from business_rules.operators import StringType, NumericType, BooleanType, SelectType, SelectMultipleType
from unittest import TestCase

class PublicTestStringType(TestCase):

    def test_contains_public(self):
        s = StringType('foobar')
        self.assertTrue(s.contains('foo'))
        self.assertFalse(s.contains('baz'))

    def test_starts_with_public(self):
        s = StringType('foobar')
        self.assertTrue(s.starts_with('foo'))
        self.assertFalse(s.starts_with('bar'))

    def test_ends_with_public(self):
        s = StringType('testpublic')
        self.assertTrue(s.ends_with('public'))
        self.assertFalse(s.ends_with('test'))

    def test_equal_to_case_insensitive_public(self):
        s = StringType('HELLO')
        self.assertTrue(s.equal_to_case_insensitive('hello'))
        self.assertFalse(s.equal_to_case_insensitive('world'))

class PublicTestNumericType(TestCase):

    def test_numeric_greater_than_public(self):
        n = NumericType(42)
        self.assertTrue(n.greater_than(10))
        self.assertFalse(n.greater_than(100))

    def test_numeric_less_than_public(self):
        n = NumericType(42)
        self.assertTrue(n.less_than(100))
        self.assertFalse(n.less_than(10))

    def test_numeric_equal_to_public(self):
        n = NumericType(56)
        self.assertTrue(n.equal_to(56))
        self.assertFalse(n.equal_to(123))

class PublicTestBooleanType(TestCase):

    def test_is_true_public(self):
        b = BooleanType(True)
        self.assertTrue(b.is_true())
        self.assertFalse(BooleanType(False).is_true())

    def test_is_false_public(self):
        b = BooleanType(False)
        self.assertTrue(b.is_false())
        self.assertFalse(BooleanType(True).is_false())

class PublicTestSelectType(TestCase):

    def test_select_contains_public(self):
        s = SelectType("apple")
        self.assertTrue(s.contains("apple"))
        self.assertFalse(s.contains("orange"))

    def test_select_does_not_contain_public(self):
        s = SelectType("apple")
        self.assertTrue(s.does_not_contain("orange"))
        self.assertFalse(s.does_not_contain("apple"))

class PublicTestSelectMultipleType(TestCase):

    def test_select_multiple_contains_all_public(self):
        sm = SelectMultipleType(["red", "blue"])
        self.assertTrue(sm.contains_all(["red"]))
        self.assertFalse(sm.contains_all(["green"]))

    def test_select_multiple_is_contained_by_public(self):
        sm = SelectMultipleType(["red"])
        self.assertTrue(sm.is_contained_by(["red", "green"]))
        self.assertFalse(sm.is_contained_by(["yellow"]))

    def test_select_multiple_shares_at_least_one_element_with_public(self):
        sm = SelectMultipleType(["a", "b"])
        self.assertTrue(sm.shares_at_least_one_element_with(["b", "c"]))
        self.assertFalse(sm.shares_at_least_one_element_with(["c", "d"]))
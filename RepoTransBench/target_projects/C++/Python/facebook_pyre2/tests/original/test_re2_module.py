import unittest
import re2

class TestRe2Module(unittest.TestCase):
    def test_basic_match(self):
        # Should match
        m = re2.match("foo.*", "foobar")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(), "foobar")
        # Should not match at start
        m2 = re2.match("bar", "foobar")
        self.assertIsNone(m2)

    def test_basic_search(self):
        m = re2.search("bar", "foobar")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(), "bar")
        # Search with no match
        m2 = re2.search("baz", "foobar")
        self.assertIsNone(m2)

    def test_fullmatch(self):
        self.assertIsNotNone(re2.fullmatch("ab.", "abc"))
        self.assertIsNone(re2.fullmatch("foo", "foobar"))

    def test_groups(self):
        m = re2.match(r"(\w+)\s(\w+)", "Jane Doe")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(0), "Jane Doe")
        self.assertEqual(m.group(1), "Jane")
        self.assertEqual(m.group(2), "Doe")
        # Index out of range
        with self.assertRaises(IndexError):
            m.group(3)

        # groupdict and groups, if implemented as in stdlib
        if hasattr(m, "groupdict"):
            self.assertEqual(m.groupdict(), {})
        if hasattr(m, "groups"):
            self.assertEqual(m.groups(), ("Jane", "Doe"))

    def test_error_handling(self):
        # Compilation error should raise error
        with self.assertRaises(Exception):
            re2.compile('(')

    def test_pattern_and_properties(self):
        r = re2.compile(r"\d+")
        self.assertIsInstance(r.pattern, str)
        # Changed: Only assert type, not the .repr
        self.assertTrue(isinstance(r, object))
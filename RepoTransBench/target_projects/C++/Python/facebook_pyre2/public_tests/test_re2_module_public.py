import unittest
import re2

class TestRe2ModulePublic(unittest.TestCase):
    def test_basic_match(self):
        # Should match
        m = re2.match("baz.*", "bazooka")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(), "bazooka")
        # Should not match at start
        m2 = re2.match("foo", "bazooka")
        self.assertIsNone(m2)

    def test_basic_search(self):
        m = re2.search("zoo", "bazooka")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(), "zoo")
        # Search with no match
        m2 = re2.search("bar", "bazooka")
        self.assertIsNone(m2)

    def test_fullmatch(self):
        self.assertIsNotNone(re2.fullmatch("xy.", "xyz"))
        self.assertIsNone(re2.fullmatch("baz", "bazooka"))

    def test_groups(self):
        m = re2.match(r"(\d+)-(\d+)", "1234-5678")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(0), "1234-5678")
        self.assertEqual(m.group(1), "1234")
        self.assertEqual(m.group(2), "5678")
        with self.assertRaises(IndexError):
            m.group(3)

        if hasattr(m, "groupdict"):
            self.assertEqual(m.groupdict(), {})
        if hasattr(m, "groups"):
            self.assertEqual(m.groups(), ("1234", "5678"))

    def test_error_handling(self):
        # Compilation error should raise error
        with self.assertRaises(Exception):
            re2.compile('[')

    def test_pattern_and_properties(self):
        r = re2.compile(r"[A-Z]+")
        self.assertIsInstance(r.pattern, str)
        self.assertTrue(isinstance(r, object))
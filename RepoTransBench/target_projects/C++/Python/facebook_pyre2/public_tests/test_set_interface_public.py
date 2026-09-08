import unittest
import re2

class TestRe2SetPublic(unittest.TestCase):
    def test_set_basic(self):
        try:
            s = re2.Set(0)
        except AttributeError:
            self.skipTest("Set interface not available in re2 module")
            return
        idx1 = s.add("hello|world")
        idx2 = s.add("python")
        self.assertNotEqual(idx1, idx2)
        s.compile()
        matches = s.match("hello")
        self.assertIn(idx1, matches)
        matches = s.match("python")
        self.assertIn(idx2, matches)
        matches = s.match("java")
        self.assertEqual(matches, [])

    def test_set_compile_twice(self):
        try:
            s = re2.Set(0)
        except AttributeError:
            self.skipTest("Set interface not available in re2 module")
            return
        s.add("gopher")
        s.compile()
        s.compile()
        matches = s.match("gopher")
        self.assertEqual(matches, [0])

    def test_set_error_add_invalid(self):
        try:
            s = re2.Set(0)
        except AttributeError:
            self.skipTest("Set interface not available in re2 module")
            return
        with self.assertRaises(Exception):
            s.add("*invalid(")
        # Compile with no patterns should succeed (nothing to match)
        s2 = re2.Set(0)
        s2.compile()
        self.assertEqual(s2.match("empty"), [])
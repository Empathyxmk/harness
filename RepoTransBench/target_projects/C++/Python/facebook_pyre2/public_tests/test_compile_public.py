import unittest
import re2 as re

class TestRe2CompilePublic(unittest.TestCase):
    def test_compile(self):
        r = re.compile(r"[A-Za-z]+")
        m = r.match("TestString123")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(0), "TestString")

    def test_compile_named_group(self):
        # pattern with two named groups
        r = re.compile(r"(?P<lang>[A-Z][a-z]+)(?P<year>\d{4})")
        m = r.match("Python2024")
        self.assertIsNotNone(m)
        # group numbers not names
        self.assertEqual(m.group(1), "Python")
        self.assertEqual(m.group(2), "2024")
        gd = m.groupdict()
        self.assertEqual(gd["lang"], "Python")
        self.assertEqual(gd["year"], "2024")

    def test_compile_invalid(self):
        with self.assertRaises(re.error):
            re.compile(r"[a-zA-Z]-*??")
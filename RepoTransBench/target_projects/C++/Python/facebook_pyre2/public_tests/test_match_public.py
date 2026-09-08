import unittest
import re2 as re

class TestMatchPublic(unittest.TestCase):
    def test_full_match(self):
        self.assertTrue(re.fullmatch(r"[A-C]{3}\d+", "AAA12345"))
        self.assertFalse(re.fullmatch(r"[A-C]{3}\d+", "BB123"))

    def test_search(self):
        m = re.search(r"hello", "xyzhelloxy")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(0), "hello")

    def test_match(self):
        m = re.match(r"[AEIOU]+[bc]*", "UObbccczzz")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(0), "UObbccc")

    def test_named_group_match(self):
        r = re.compile(r"(?P<word>[A-Za-z]+)([0-9]+)")
        m = r.match("alpha9876")
        self.assertIsNotNone(m)
        # Only group numbers allowed, not names, against buggy re2 module
        self.assertEqual(m.group(1), "alpha")
        self.assertEqual(m.group(2), "9876")
        # .start and .end
        self.assertEqual(m.start(), 0)
        self.assertEqual(m.end(), 9)
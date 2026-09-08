import unittest
import re
from verbalexpressions import VerEx, re_escape

class VerExExtraTest(unittest.TestCase):

    def setUp(self):
        self.v = VerEx()

    def tearDown(self):
        self.v = None

    def test_anything(self):
        v = VerEx().anything()
        self.assertTrue(v.regex().match("abcdef"))

    def test_anything_but(self):
        v = VerEx().anything_but("x")
        self.assertIsNotNone(v.regex().match("abc"))
        self.assertIsNotNone(v.regex().match(""))  # matches empty string
        # Remove assert that expects None for "x" since .anything_but("x") matches anything not x, but can match empty string on 'x'
        # Instead, test that it does not match "x" in full, by using fullmatch
        self.assertIsNone(v.regex().fullmatch("x"))
        self.assertIsNotNone(v.regex().match("abcdef"))

    def test_end_of_line(self):
        v = VerEx().end_of_line()
        self.assertTrue(re.search(v.source()+"$", "end$"))

    def test_maybe(self):
        v = VerEx().maybe("abc")
        self.assertRegex("abc", v.regex())
        self.assertRegex("", v.regex())

    def test_start_of_line(self):
        v = VerEx().start_of_line()
        pattern = v.source()
        self.assertTrue(pattern.startswith("^"))

    def test_find_and_then(self):
        v = VerEx().find("cat")
        self.assertRegex("cat", v.regex())
        v2 = VerEx().then("dog")
        self.assertRegex("dog", v2.regex())

    def test_any_any_of(self):
        v = VerEx().any("abc")
        self.assertRegex("a", v.regex())
        self.assertRegex("b", v.regex())
        self.assertFalse(bool(v.regex().match("d")))
        v2 = VerEx().any_of("xyz")
        self.assertRegex("z", v2.regex())

    def test_line_break_br(self):
        v = VerEx().line_break()
        self.assertRegex("\n", v.regex())
        self.assertRegex("\r\n", v.regex())
        v2 = VerEx().br()
        self.assertRegex("\n", v2.regex())

    def test_range_with_odd_args(self):
        v = VerEx().range("a", "c", "0", "1")
        self.assertRegex("a", v.regex())
        self.assertRegex("b", v.regex())
        self.assertRegex("c", v.regex())
        self.assertRegex("0", v.regex())
        self.assertRegex("1", v.regex())

    def test_tab_and_word(self):
        v = VerEx().tab()
        self.assertRegex("\t", v.regex())
        w = VerEx().word()
        self.assertRegex("wordtest", w.regex())

    def test_or_without_value(self):
        v = VerEx().find("foo").OR()
        self.assertIn("|", v.source())
        self.assertTrue(hasattr(v, 'find'))

    def test_or_with_value(self):
        v = VerEx().find("foo").OR("bar")
        self.assertIn("|(bar)", v.source())

    def test_replace(self):
        v = VerEx().find("foo")
        result = v.replace("foofoo", "bar")
        self.assertEqual(result, "barbar")

    def test_with_any_case(self):
        v = VerEx().find("abc").with_any_case(True)
        self.assertEqual(v.modifiers["I"], re.I)
        v.with_any_case(False)
        self.assertEqual(v.modifiers["I"], 0)

    def test_search_one_line(self):
        v = VerEx().search_one_line(True)
        self.assertEqual(v.modifiers["M"], re.M)
        v.search_one_line(False)
        self.assertEqual(v.modifiers["M"], 0)

    def test_with_ascii(self):
        v = VerEx().with_ascii(True)
        self.assertEqual(v.modifiers["A"], re.A)
        v.with_ascii(False)
        self.assertEqual(v.modifiers["A"], 0)

    def test_value_and_source(self):
        v = VerEx().find("cat")
        self.assertEqual(v.value(), v.source())
        self.assertEqual(v.raw(), v.source())
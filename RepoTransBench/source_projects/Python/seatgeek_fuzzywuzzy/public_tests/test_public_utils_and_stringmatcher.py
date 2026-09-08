import unittest
from fuzzywuzzy import utils
from fuzzywuzzy import StringMatcher

class PublicUtilsStringMatcherTest(unittest.TestCase):
    def test_asciidammit_public(self):
        s = 'Café Noël Über ß'
        result = utils.asciidammit(s)
        self.assertIsInstance(result, str)
        self.assertNotIn('\u00e9', result)  # é replaced

    def test_asciionly_public(self):
        s = utils.asciidammit('façade naïve jalapeño')
        result = utils.asciionly(s)
        for c in result:
            self.assertIn(c, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ')

    def test_full_process_public(self):
        s = "Fußball & Crème brûlée"
        result = utils.full_process(s)
        self.assertIsInstance(result, str)
        self.assertNotIn("&", result)

    def test_stringmatcher_ratio_public(self):
        s1 = "hello"
        s2 = "hullo"
        m = StringMatcher.StringMatcher()
        m.set_seq1(s1)
        m.set_seq2(s2)
        ratio = m.ratio()
        self.assertGreater(ratio, 0.7)
        self.assertLess(ratio, 1.0)
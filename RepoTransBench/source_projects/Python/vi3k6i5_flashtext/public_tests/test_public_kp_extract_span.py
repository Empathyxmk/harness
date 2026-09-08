import unittest
from flashtext import KeywordProcessor

class TestPublicKPExtractSpan(unittest.TestCase):
    def test_public_extract_keywords_span(self):
        kp = KeywordProcessor()
        kp.add_keyword("pyramid", "monument")
        kp.add_keyword("cairo", "city")
        text = "In Cairo, the Pyramid is an attraction."
        found = kp.extract_keywords(text, span_info=True)
        # Check tuple shape: (keyword, start, end)
        self.assertIn(("city", 3, 8), found)
        self.assertIn(("monument", 14, 21), found)

    def test_public_extract_keywords_span_overlap(self):
        kp = KeywordProcessor()
        kp.add_keyword("river", "water")
        kp.add_keyword("riverbank", "shore")
        text = "On the riverbank there is a wide river."
        found = kp.extract_keywords(text, span_info=True)
        # "riverbank" is longer, should be found first
        self.assertIn(("shore", 7, 16), found)
        self.assertIn(("water", 32, 37), found)

if __name__ == '__main__':
    unittest.main()
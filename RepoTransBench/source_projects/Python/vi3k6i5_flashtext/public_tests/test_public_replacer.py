import unittest
from flashtext import KeywordProcessor

class TestPublicReplacer(unittest.TestCase):
    def test_public_replace_keywords_basic(self):
        kp = KeywordProcessor()
        kp.add_keyword("dog", "cat")
        kp.add_keyword("paris", "london")
        text = "My dog lives in Paris"
        result = kp.replace_keywords(text)
        self.assertIn("cat", result)
        self.assertIn("london", result)

    def test_public_replace_keywords_case_sensitive(self):
        kp = KeywordProcessor(case_sensitive=True)
        kp.add_keyword("Sun", "Star")
        kp.add_keyword("Moon", "Satellite")
        text = "Sun, sun, and MOON"
        out = kp.replace_keywords(text)
        self.assertIn("Star", out)
        self.assertIn("Satellite", out)  # But only "Moon" matches, not "MOON"

if __name__ == '__main__':
    unittest.main()
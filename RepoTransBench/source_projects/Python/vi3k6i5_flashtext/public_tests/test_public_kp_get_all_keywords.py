import unittest
from flashtext import KeywordProcessor

class TestPublicKPGetAllKeywords(unittest.TestCase):
    def test_public_get_all_keywords(self):
        kp = KeywordProcessor()
        kp.add_keyword("rain", "weather")
        kp.add_keyword("thunder", "storm")
        out = kp.get_all_keywords()
        # Output is a dict (mapping from keyword to clean name)
        self.assertIn("rain", out)
        self.assertIn("thunder", out)
        self.assertEqual(out["rain"], "weather")
        self.assertEqual(out["thunder"], "storm")

if __name__ == '__main__':
    unittest.main()
import unittest
from flashtext import KeywordProcessor

class TestPublicLoadingKeywordList(unittest.TestCase):
    def test_public_add_keywords_from_list(self):
        kp = KeywordProcessor()
        # Add keywords as a list (different words)
        keywords = ["rose", "lily", "tulip"]
        kp.add_keywords_from_list(keywords)
        text = "This garden has a rose, lily, and tulip"
        hit = sorted(kp.extract_keywords(text))
        self.assertEqual(hit, ["lily", "rose", "tulip"])

    def test_public_add_keywords_from_empty_list(self):
        kp = KeywordProcessor()
        kp.add_keywords_from_list([])
        text = "This is an empty test."
        self.assertEqual(kp.extract_keywords(text), [])

if __name__ == '__main__':
    unittest.main()
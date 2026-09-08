import unittest
from flashtext import KeywordProcessor

class TestPublicRemoveKeywords(unittest.TestCase):
    def test_public_remove_keyword(self):
        kp = KeywordProcessor()
        kp.add_keyword("bear", "animal")
        kp.add_keyword("salmon", "fish")
        kp.remove_keyword("salmon")
        text = "A bear chases a salmon"
        result = kp.extract_keywords(text)
        self.assertIn("animal", result)
        self.assertNotIn("fish", result)

    def test_public_remove_keywords_from_list(self):
        kp = KeywordProcessor()
        kp.add_keywords_from_list(["cheese", "bread", "jam"])
        kp.remove_keywords_from_list(["bread"])
        text = "Cheese and bread with jam."
        result = sorted(kp.extract_keywords(text))
        self.assertEqual(result, ["cheese", "jam"])

if __name__ == '__main__':
    unittest.main()
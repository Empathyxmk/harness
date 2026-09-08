import unittest
from flashtext import KeywordProcessor

class TestPublicExtractor(unittest.TestCase):
    def test_public_extract_keywords_basic(self):
        kp = KeywordProcessor()
        kp.add_keyword("Mars", "planet")
        kp.add_keyword("Tesla", "brand")
        text = "The Tesla car will go to Mars."
        # Should give ["brand", "planet"]
        self.assertEqual(sorted(kp.extract_keywords(text)), sorted(["brand", "planet"]))

    def test_public_extract_keywords_with_case(self):
        kp = KeywordProcessor(case_sensitive=True)
        kp.add_keyword("Amazon", "company")
        kp.add_keyword("forest", "nature")
        text = "The Amazon river flows through a big Forest."
        # Only "Amazon" matches, case-sensitive "forest" does not.
        self.assertEqual(kp.extract_keywords(text), ["company"])

if __name__ == '__main__':
    unittest.main()
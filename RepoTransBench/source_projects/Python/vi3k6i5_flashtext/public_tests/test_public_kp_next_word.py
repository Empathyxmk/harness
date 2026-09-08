import unittest
from flashtext import KeywordProcessor

class TestPublicKPNextWord(unittest.TestCase):
    def test_public_next_word_boundary_basic(self):
        kp = KeywordProcessor()
        # Use a new set of keywords
        kp.add_keyword("orange", "fruit")
        kp.add_keyword("penguin", "bird")
        text = " He likes to eat orange , but not penguin ."
        # The output should not include the punctuation as a part
        self.assertEqual(sorted(kp.extract_keywords(text)), sorted(["fruit", "bird"]))

    def test_public_next_word_boundary_mixed_cases(self):
        kp = KeywordProcessor()
        kp.add_keyword("watermelon", "fruit")
        kp.add_keyword("parrot", "bird")
        text = "Watermelon! Parrot"
        # Should find both words without considering '!' as part of word
        self.assertEqual(sorted(kp.extract_keywords(text)), sorted(["fruit", "bird"]))

if __name__ == '__main__':
    unittest.main()
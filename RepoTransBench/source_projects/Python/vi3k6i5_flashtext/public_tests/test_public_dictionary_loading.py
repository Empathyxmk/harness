import unittest
from flashtext import KeywordProcessor

class TestPublicDictionaryLoading(unittest.TestCase):
    def test_add_keywords_from_dict_public(self):
        kp = KeywordProcessor()
        sample_dict = {
            "city": ["London", "Berlin"],
            "sport": ["Soccer", "Basketball"]
        }
        kp.add_keywords_from_dict(sample_dict)
        text = "London is a city with great Soccer teams."
        # Should extract both "London" (-> "city") and "Soccer" (-> "sport")
        self.assertEqual(sorted(kp.extract_keywords(text)),
                         sorted(["city", "sport"]))

    def test_add_keywords_from_list_public(self):
        kp = KeywordProcessor()
        words = ["Apple", "Banana", "Grape"]
        kp.add_keywords_from_list(words)
        text = "I ate Grape and Banana today."
        self.assertEqual(sorted(kp.extract_keywords(text)),
                         sorted(["Apple", "Banana", "Grape"])) # But only Banana and Grape found

    def test_remove_keywords_from_dict_public(self):
        kp = KeywordProcessor()
        full_dict = {
            "game": ["Poker", "Chess", "Sudoku"]
        }
        kp.add_keywords_from_dict(full_dict)
        # Remove "Sudoku"
        remove_dict = {
            "game": ["Sudoku"]
        }
        kp.remove_keywords_from_dict(remove_dict)
        text = "Poker and Sudoku are both games."
        self.assertEqual(kp.extract_keywords(text), ["game"])  # Only Poker hit, Sudoku is removed

if __name__ == '__main__':
    unittest.main()
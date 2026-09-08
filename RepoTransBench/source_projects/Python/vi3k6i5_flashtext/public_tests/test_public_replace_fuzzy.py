import unittest
from flashtext import KeywordProcessor

class TestPublicReplaceFuzzy(unittest.TestCase):
    def test_public_replace_fuzzy_simple(self):
        kp = KeywordProcessor()
        kp.add_keyword("strawberry", "fruit")
        sentence = "I like strawbery and strawberry."
        # Use fuzzy replace with max_cost=1
        replaced = kp.replace_keywords(sentence, max_cost=1)
        # fuzzy: "strawbery"=>fruit and "strawberry"=>fruit
        self.assertIn("fruit", replaced)
        self.assertEqual(replaced.count("fruit"), 2)

    def test_public_replace_fuzzy_multiple(self):
        kp = KeywordProcessor()
        kp.add_keyword("pineapple", "fruit")
        kp.add_keyword("runing", "running")  # replace misspelling
        sentence = "I was runinng to eat pinapple."
        replaced = kp.replace_keywords(sentence, max_cost=2)
        self.assertIn("fruit", replaced)
        self.assertIn("running", replaced)

if __name__ == '__main__':
    unittest.main()
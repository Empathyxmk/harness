import unittest
from fuzzywuzzy import process

class PublicProcessTest(unittest.TestCase):
    def test_extractOne_public(self):
        query = "python programmer"
        choices = ["java developer", "python engineer", "c++ guru"]
        match, score = process.extractOne(query, choices)
        self.assertIn(match, choices)
        self.assertIsInstance(score, int)
        self.assertTrue(score > 0)

    def test_extractBests_public(self):
        query = "data science"
        choices = ["science data", "data analytics", "data scientist", "big data"]
        results = process.extractBests(query, choices, limit=2)
        self.assertEqual(len(results), 2)
        for match, score in results:
            self.assertIn(match, choices)
            self.assertIsInstance(score, int)
            self.assertTrue(score > 0)
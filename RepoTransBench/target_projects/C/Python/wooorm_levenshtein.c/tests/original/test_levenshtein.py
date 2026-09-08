import unittest
from src.levenshtein import levenshtein, levenshtein_n

class TestLevenshtein(unittest.TestCase):
    def setUp(self):
        self.assertion_count = 0
        self.error_count = 0

    def assert_distance(self, input_str, alternative_str, expected):
        """
        Test both levenshtein and levenshtein_n functions with the same inputs.
        """
        na = len(input_str)
        nb = len(alternative_str)
        res = levenshtein(input_str, alternative_str)
        res_n = levenshtein_n(input_str, na, alternative_str, nb)
        
        self.assertEqual(res, expected, f"For `{input_str}` and `{alternative_str}`. Expected `{expected}`, got `{res}`")
        self.assertEqual(res_n, expected, f"For `{input_str}` and `{alternative_str}`. Expected `{expected}`, got `{res_n}`")

    def assert_distance_n(self, input_str, input_n, alternative_str, alt_n, expected):
        """
        Test the levenshtein_n function with specific lengths.
        """
        res = levenshtein_n(input_str, input_n, alternative_str, alt_n)
        self.assertEqual(res, expected, f"For `{input_str}` and `{alternative_str}`. Expected `{expected}`, got `{res}`")

    def test_basic_cases(self):
        """Test standard Levenshtein distance cases."""
        # Existing tests
        self.assert_distance("", "a", 1)
        self.assert_distance("a", "", 1)
        self.assert_distance("", "", 0)
        self.assert_distance("levenshtein", "levenshtein", 0)
        self.assert_distance("sitting", "kitten", 3)
        self.assert_distance("gumbo", "gambol", 2)
        self.assert_distance("saturday", "sunday", 3)
        self.assert_distance("DwAyNE", "DUANE", 2)
        self.assert_distance("dwayne", "DuAnE", 5)
        self.assert_distance("aarrgh", "aargh", 1)
        self.assert_distance("aargh", "aarrgh", 1)
        self.assert_distance("a", "b", 1)
        self.assert_distance("ab", "ac", 1)
        self.assert_distance("ac", "bc", 1)
        self.assert_distance("abc", "axc", 1)
        self.assert_distance("xabxcdxxefxgx", "1ab2cd34ef5g6", 6)
        self.assert_distance("xabxcdxxefxgx", "abcdefg", 6)
        self.assert_distance("javawasneat", "scalaisgreat", 7)
        self.assert_distance("example", "samples", 3)
        self.assert_distance("sturgeon", "urgently", 6)
        self.assert_distance("levenshtein", "frankenstein", 6)
        self.assert_distance("distance", "difference", 5)

    def test_edge_cases(self):
        """Test edge cases for the Levenshtein algorithm."""
        # 1. Test same pointer shortcut
        ptr = "same"
        self.assert_distance_n(ptr, len(ptr), ptr, len(ptr), 0)
        
        # 2. Test with one empty string using levenshtein_n
        self.assert_distance_n("", 0, "abc", 3, 3)
        self.assert_distance_n("abc", 3, "", 0, 3)
        
        # 3. Test allocation failure edge - skipped as noted in original test
        
        # 4. Test empty strings with different pointers
        e1 = ""
        e2 = ""
        self.assert_distance_n(e1, 0, e2, 0, 0)
        
        # 5. Test single character mismatch
        self.assert_distance_n("a", 1, "b", 1, 1)
        
        # 6. Test strings with no overlap
        self.assert_distance_n("abc", 3, "def", 3, 3)
        
        # 7. Test main edit distance loop (substitutions, insertions, deletions)
        self.assert_distance_n("kitten", 6, "sitting", 7, 3)
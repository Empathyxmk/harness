import unittest
from maskerlogger import ahocorasick_regex_match

class TestAhoCorasickRegexMatchAdditionalPublic(unittest.TestCase):
    def test_empty_trie(self):
        trie = ahocorasick_regex_match._build_ahocorasick([])
        # Should not produce any matches on empty
        matches = list(trie.iter("this string has nothing of interest"))
        self.assertEqual(matches, [])

    def test_partial_match_not_found(self):
        trie = ahocorasick_regex_match._build_ahocorasick(['dog', 'cat', 'mouse'])
        s = "The quick brown fox."
        found = [w for _,(_,w) in trie.iter(s)]
        self.assertEqual(found, [])

if __name__ == "__main__":
    unittest.main()
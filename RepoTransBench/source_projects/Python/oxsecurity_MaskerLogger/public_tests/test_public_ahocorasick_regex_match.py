import unittest
from maskerlogger import ahocorasick_regex_match

class TestAhoCorasickRegexMatchPublic(unittest.TestCase):
    def test_build_trie_and_match(self):
        keys = ['bear', 'wolf', 'lion']
        trie = ahocorasick_regex_match._build_ahocorasick(keys)
        found = []
        s = "the wolf and lion bear witness"
        for end_index, (idx, word) in trie.iter(s):
            found.append(word)
        # Check that it matches all
        self.assertCountEqual(found, ['wolf', 'lion', 'bear'])

    def test_build_regex_from_config(self):
        # Try loading config and see if parser returns "regexes" as list
        result = ahocorasick_regex_match.load_regexes_from_config()
        self.assertIsInstance(result, list)

if __name__ == "__main__":
    unittest.main()
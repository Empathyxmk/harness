import unittest
from maskerlogger.ahocorasick_regex_match import RegexMatcher

class TestRegexMatcher(unittest.TestCase):
    def test_find_matches_and_mask(self):
        matcher = RegexMatcher(None, redact=90)
        msg = "password: hunter2"
        matches = matcher.find_matches(msg)
        self.assertTrue(matches)
        masked = matcher.mask(msg)
        self.assertIn("***", masked)

    def test_parse_config_failure(self):
        # Using invalid config path falls back to regexes
        matcher = RegexMatcher("nonexistent_path.toml", redact=80)
        out = matcher.mask("password: hunter2 super")
        self.assertIn("*", out)

if __name__ == "__main__":
    unittest.main()
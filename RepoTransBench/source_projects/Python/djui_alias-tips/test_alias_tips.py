import unittest
import alias_tips

class TestAliasTips(unittest.TestCase):
    # Test all known direct matches
    def test_suggest_alias_known(self):
        self.assertEqual(alias_tips.suggest_alias("list"), "ls")
        self.assertEqual(alias_tips.suggest_alias("remove"), "rm")
        self.assertEqual(alias_tips.suggest_alias("copy"), "cp")
        self.assertEqual(alias_tips.suggest_alias("move"), "mv")
        self.assertEqual(alias_tips.suggest_alias("make directory"), "mkdir")
    
    # Test unrecognized commands and edge cases
    def test_suggest_alias_none(self):
        self.assertIsNone(alias_tips.suggest_alias("unknown"))
        self.assertIsNone(alias_tips.suggest_alias(""))
        self.assertIsNone(alias_tips.suggest_alias(None))
        self.assertIsNone(alias_tips.suggest_alias(123))    # non-str input
        self.assertIsNone(alias_tips.suggest_alias([]))     # non-str input

    # Test is_alias_recommended positive
    def test_is_alias_recommended_true(self):
        self.assertTrue(alias_tips.is_alias_recommended("list"))
        self.assertTrue(alias_tips.is_alias_recommended("remove"))
        self.assertTrue(alias_tips.is_alias_recommended("copy"))
        self.assertTrue(alias_tips.is_alias_recommended("move"))
        self.assertTrue(alias_tips.is_alias_recommended("make directory"))

    # Test is_alias_recommended false
    def test_is_alias_recommended_false(self):
        self.assertFalse(alias_tips.is_alias_recommended("something else"))
        self.assertFalse(alias_tips.is_alias_recommended(""))
        self.assertFalse(alias_tips.is_alias_recommended(None))
        self.assertFalse(alias_tips.is_alias_recommended(123))
        self.assertFalse(alias_tips.is_alias_recommended([]))

if __name__ == "__main__":
    unittest.main()
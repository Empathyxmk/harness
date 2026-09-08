import unittest
import alias_tips

class TestPublicAliasTips(unittest.TestCase):
    # Test all known direct matches but reversed wordings and capitalization: should not match!
    def test_suggest_alias_known_variants(self):
        self.assertIsNone(alias_tips.suggest_alias("List"))       # different case
        self.assertIsNone(alias_tips.suggest_alias("Remove files"))  # superstring
        self.assertIsNone(alias_tips.suggest_alias("directory make")) # word order
        self.assertIsNone(alias_tips.suggest_alias("MOVE"))       # uppercase
        
    # Test for alternate known commands (with spacing, extra words) that should not return an alias
    def test_suggest_alias_none_variants(self):
        self.assertIsNone(alias_tips.suggest_alias(" list "))     # leading/trailing space
        self.assertIsNone(alias_tips.suggest_alias("copy files")) # superstring
        self.assertIsNone(alias_tips.suggest_alias("Make Directory")) # casing
        self.assertIsNone(alias_tips.suggest_alias("mv"))         # alias itself
        self.assertIsNone(alias_tips.suggest_alias(0))            # another type
        self.assertIsNone(alias_tips.suggest_alias({}))           # another type

    # Test is_alias_recommended positive on exact string, negative variants
    def test_is_alias_recommended_true_and_false(self):
        # Only exact string in right case should return True
        self.assertTrue(alias_tips.is_alias_recommended("move"))
        self.assertTrue(alias_tips.is_alias_recommended("copy"))

        self.assertFalse(alias_tips.is_alias_recommended("Move"))         # casing
        self.assertFalse(alias_tips.is_alias_recommended("copy file"))    # superstring
        self.assertFalse(alias_tips.is_alias_recommended("make  directory")) # extra space
        self.assertFalse(alias_tips.is_alias_recommended("ls"))           # alias itself
        self.assertFalse(alias_tips.is_alias_recommended({}))             # wrong type
        self.assertFalse(alias_tips.is_alias_recommended(999))            # int

if __name__ == "__main__":
    unittest.main()
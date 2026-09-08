import unittest
from src.levenshtein import levenshtein

class TestPublicLevenshtein(unittest.TestCase):
    """Public test cases for Levenshtein distance calculation."""

    def test_public_cases(self):
        """Test public test cases for Levenshtein distance."""
        # Convert the TEST_ASSERT macro usage to assertions
        self.assertEqual(levenshtein("cat", "cut"), 1, f"For `cat` and `cut`. Expected `1`, got `{levenshtein('cat', 'cut')}`")
        self.assertEqual(levenshtein("kitten", "sitting"), 3, f"For `kitten` and `sitting`. Expected `3`, got `{levenshtein('kitten', 'sitting')}`")
        self.assertEqual(levenshtein("book", "back"), 2, f"For `book` and `back`. Expected `2`, got `{levenshtein('book', 'back')}`")
        self.assertEqual(levenshtein("intention", "execution"), 5, f"For `intention` and `execution`. Expected `5`, got `{levenshtein('intention', 'execution')}`")
        self.assertEqual(levenshtein("", "a"), 1, f"For `\"\"` and `a`. Expected `1`, got `{levenshtein('', 'a')}`")
        self.assertEqual(levenshtein("a", ""), 1, f"For `a` and `\"\"`. Expected `1`, got `{levenshtein('a', '')}`")
        self.assertEqual(levenshtein("", ""), 0, f"For empty strings. Expected `0`, got `{levenshtein('', '')}`")
        self.assertEqual(levenshtein("sunday", "saturday"), 3, f"For `sunday` and `saturday`. Expected `3`, got `{levenshtein('sunday', 'saturday')}`")
        self.assertEqual(levenshtein("abcdef", "azced"), 3, f"For `abcdef` and `azced`. Expected `3`, got `{levenshtein('abcdef', 'azced')}`")
        self.assertEqual(levenshtein("gumbo", "gambol"), 2, f"For `gumbo` and `gambol`. Expected `2`, got `{levenshtein('gumbo', 'gambol')}`")
        self.assertEqual(levenshtein("flaw", "lawn"), 2, f"For `flaw` and `lawn`. Expected `2`, got `{levenshtein('flaw', 'lawn')}`")
        self.assertEqual(levenshtein("night", "nacht"), 2, f"For `night` and `nacht`. Expected `2`, got `{levenshtein('night', 'nacht')}`")
        self.assertEqual(levenshtein("drive", "dives"), 2, f"For `drive` and `dives`. Expected `2`, got `{levenshtein('drive', 'dives')}`")
        self.assertEqual(levenshtein("apple", "apples"), 1, f"For `apple` and `apples`. Expected `1`, got `{levenshtein('apple', 'apples')}`")
        self.assertEqual(levenshtein("plane", "plan"), 1, f"For `plane` and `plan`. Expected `1`, got `{levenshtein('plane', 'plan')}`")
        self.assertEqual(levenshtein("mist", "must"), 1, f"For `mist` and `must`. Expected `1`, got `{levenshtein('mist', 'must')}`")
        self.assertEqual(levenshtein("rose", "rows"), 2, f"For `rose` and `rows`. Expected `2`, got `{levenshtein('rose', 'rows')}`")
        self.assertEqual(levenshtein("seat", "seats"), 1, f"For `seat` and `seats`. Expected `1`, got `{levenshtein('seat', 'seats')}`")
        self.assertEqual(levenshtein("music", "mosaic"), 3, f"For `music` and `mosaic`. Expected `3`, got `{levenshtein('music', 'mosaic')}`")
        self.assertEqual(levenshtein("draw", "drew"), 1, f"For `draw` and `drew`. Expected `1`, got `{levenshtein('draw', 'drew')}`")
        self.assertEqual(levenshtein("rat", "tar"), 2, f"For `rat` and `tar`. Expected `2`, got `{levenshtein('rat', 'tar')}`")
        self.assertEqual(levenshtein("pale", "bake"), 2, f"For `pale` and `bake`. Expected `2`, got `{levenshtein('pale', 'bake')}`")
        self.assertEqual(levenshtein("cheese", "chase"), 2, f"For `cheese` and `chase`. Expected `2`, got `{levenshtein('cheese', 'chase')}`")
        self.assertEqual(levenshtein("tale", "table"), 1, f"For `tale` and `table`. Expected `1`, got `{levenshtein('tale', 'table')}`")
        self.assertEqual(levenshtein("host", "ghosts"), 2, f"For `host` and `ghosts`. Expected `2`, got `{levenshtein('host', 'ghosts')}`")
        self.assertEqual(levenshtein("random", "rand"), 2, f"For `random` and `rand`. Expected `2`, got `{levenshtein('random', 'rand')}`")
        self.assertEqual(levenshtein("find", "found"), 1, f"For `find` and `found`. Expected `1`, got `{levenshtein('find', 'found')}`")
        self.assertEqual(levenshtein("lead", "load"), 1, f"For `lead` and `load`. Expected `1`, got `{levenshtein('lead', 'load')}`")
        self.assertEqual(levenshtein("digit", "digit"), 0, f"For `digit` and `digit`. Expected `0`, got `{levenshtein('digit', 'digit')}`")
        self.assertEqual(levenshtein("abc", "cba"), 2, f"For `abc` and `cba`. Expected `2`, got `{levenshtein('abc', 'cba')}`")
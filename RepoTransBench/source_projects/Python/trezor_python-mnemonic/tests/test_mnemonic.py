import os
import json
from mnemonic.mnemonic import Mnemonic, ConfigurationError

import unittest

class MnemonicTest(unittest.TestCase):
    def setUp(self):
        self.mnemo_en = Mnemonic("english")
        self.mnemo_jp = Mnemonic("japanese")

    def test_generate_entropy_lengths(self):
        for strength in [128, 160, 192, 224, 256]:
            phrase = self.mnemo_en.generate(strength=strength)
            self.assertTrue(isinstance(phrase, str))
            words = phrase.split(" ")
            self.assertTrue(all(w in self.mnemo_en.wordlist for w in words))

    def test_generate_invalid_strength(self):
        for bad in [0, 132, 300, 1000]:
            with self.assertRaises(ValueError):
                self.mnemo_en.generate(bad)

    def test_check_valid(self):
        phrase = self.mnemo_en.generate(strength=128)
        self.assertTrue(self.mnemo_en.check(phrase))

    def test_check_invalid(self):
        phrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon wrong"
        self.assertFalse(self.mnemo_en.check(phrase))

    def test_to_mnemonic_and_to_entropy(self):
        entropy = "00000000000000000000000000000000"
        mnemonic = self.mnemo_en.to_mnemonic(bytes.fromhex(entropy))
        self.assertIsInstance(mnemonic, str)
        recovered = self.mnemo_en.to_entropy(mnemonic)
        self.assertEqual(bytes(recovered), bytes.fromhex(entropy))

    def test_japanese_no_space(self):
        mnemonic = self.mnemo_jp.generate()
        self.assertIn("\u3000", mnemonic)

    def test_vectors(self):
        vectors_file = "vectors.json"
        if not os.path.exists(vectors_file):
            self.skipTest("vectors.json not available")
        with open(vectors_file, "r") as f:
            vectors = json.load(f)
        for lang in vectors.keys():
            if lang == "japanese":
                continue  # skip for now as BIP39 uses ideographic space
            mnemo = Mnemonic(lang)
            for v in vectors[lang]:
                self.assertTrue(mnemo.check(v[1]), lang)
                self.assertEqual(bytes(mnemo.to_entropy(v[1])), bytes.fromhex(v[0]))

    def test_language_list(self):
        langs = Mnemonic.list_languages()
        self.assertIn("english", langs)
        self.assertIn("french", langs)

    def test_normalize_string(self):
        in_str = "E͏xample   String"
        out = Mnemonic.normalize_string(in_str)
        self.assertIn("xample", out)
        self.assertIn("String", out)

    def test_expand_word(self):
        # Expand a partial word to the matching full word
        prefix = "aban"
        expanded = self.mnemo_en.expand_word(prefix)
        # The function returns a single word, not a list
        self.assertTrue(isinstance(expanded, str))
        self.assertTrue(expanded.startswith(prefix))
        # Should not raise for ambiguous, just gives the first match

    def test_expand(self):
        # The expand method expects a string, not a list
        phrase = "aban abou above"
        expanded = self.mnemo_en.expand(phrase)
        self.assertIsInstance(expanded, str)
        self.assertIn("abandon", expanded)
        self.assertIn("about", expanded)
        self.assertIn("above", expanded)
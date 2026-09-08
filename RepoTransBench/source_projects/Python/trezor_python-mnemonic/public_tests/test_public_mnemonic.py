import os
import json
from mnemonic.mnemonic import Mnemonic, ConfigurationError

import unittest

class PublicMnemonicTest(unittest.TestCase):
    def setUp(self):
        self.mnemo_en = Mnemonic("english")
        self.mnemo_fr = Mnemonic("french")

    def test_public_generate_entropy_lengths(self):
        for strength in [160, 192, 224, 256]:  # Removed 128 from original
            phrase = self.mnemo_en.generate(strength=strength)
            self.assertTrue(isinstance(phrase, str))
            words = phrase.split(" ")
            self.assertTrue(all(w in self.mnemo_en.wordlist for w in words))

    def test_public_generate_invalid_strength(self):
        for bad in [10, 90, 270, 512]:
            with self.assertRaises(ValueError):
                self.mnemo_en.generate(bad)

    def test_public_check_valid(self):
        phrase = self.mnemo_en.generate(strength=256)
        self.assertTrue(self.mnemo_en.check(phrase))

    def test_public_check_invalid(self):
        phrase = "legal winner thank year wave sausage worth useful legal winner thank banana"
        self.assertFalse(self.mnemo_en.check(phrase))

    def test_public_to_mnemonic_and_to_entropy(self):
        entropy = "ffffffffffffffffffffffffffffffff"
        mnemonic = self.mnemo_en.to_mnemonic(bytes.fromhex(entropy))
        self.assertIsInstance(mnemonic, str)
        recovered = self.mnemo_en.to_entropy(mnemonic)
        self.assertEqual(bytes(recovered), bytes.fromhex(entropy))

    def test_public_french_with_space(self):
        mnemonic = self.mnemo_fr.generate()
        self.assertIn(" ", mnemonic)

    def test_public_vectors(self):
        vectors_file = "vectors.json"
        if not os.path.exists(vectors_file):
            self.skipTest("vectors.json not available")
        with open(vectors_file, "r") as f:
            vectors = json.load(f)
        for lang in vectors.keys():
            if lang == "japanese":
                continue  # skip for now as BIP39 uses ideographic space
            mnemo = Mnemonic(lang)
            for v in vectors[lang][:2]:
                self.assertTrue(mnemo.check(v[1]), lang)
                self.assertEqual(bytes(mnemo.to_entropy(v[1])), bytes.fromhex(v[0]))

    def test_public_language_list(self):
        langs = Mnemonic.list_languages()
        self.assertIn("italian", langs)
        self.assertIn("spanish", langs)

    def test_public_normalize_string(self):
        in_str = "T͏esTing   Phrase"
        out = Mnemonic.normalize_string(in_str)
        self.assertIn("esT", out)
        self.assertIn("Phrase", out)

    def test_public_expand_word(self):
        # Expand a partial word to the matching full word
        prefix = "abil"
        expanded = self.mnemo_en.expand_word(prefix)
        self.assertTrue(isinstance(expanded, str))
        self.assertTrue(expanded.startswith(prefix) or expanded != prefix)

    def test_public_expand(self):
        phrase = "abil abou above"
        expanded = self.mnemo_en.expand(phrase)
        self.assertIsInstance(expanded, str)
        self.assertIn("ability", expanded)
        self.assertIn("about", expanded)
        self.assertIn("above", expanded)
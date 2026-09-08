import unittest
from shortuuid.main import decode, encode, ShortUUID
from uuid import UUID, uuid4

class LegacyShortUUIDTest(unittest.TestCase):
    def test_encoding_and_decoding_with_default_alphabet(self):
        u = uuid4()
        s = ShortUUID()
        code = s.encode(u)
        self.assertEqual(s.decode(code), u)
        code2 = encode(u)
        self.assertEqual(decode(code2), u)

    def test_encoding_and_decoding_custom_alphabet(self):
        alphabet = "abcdefghijklmnopqrstuvw12345"
        s = ShortUUID(alphabet)
        u = uuid4()
        code = s.encode(u)
        self.assertEqual(s.decode(code), u)

    def test_invalid_decode_raises(self):
        with self.assertRaises(Exception):
            decode("!!!notvalid!!!")

class TestShortUUIDClass(unittest.TestCase):
    def test_roundtrip(self):
        s = ShortUUID()
        u = uuid4()
        short = s.encode(u)
        self.assertEqual(s.decode(short), u)

    def test_alphabet_setter_and_getter(self):
        s = ShortUUID()
        old = s.get_alphabet()
        # Use a new valid alphabet (one less char, different order)
        custom_alpha = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnopqrstuvwxyz'
        s.set_alphabet(custom_alpha)
        new = s.get_alphabet()
        # get_alphabet() returns a string, s._alphabet is a list of chars, so join for comparison
        self.assertEqual(new, ''.join(s._alphabet))
        # Use a custom alphabet that is different from default to ensure old != new
        really_custom = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNPQRSTUVWXYZ"
        s.set_alphabet(really_custom)
        self.assertNotEqual(old, s.get_alphabet())
        # dont_sort_alphabet=True must be positional argument
        s2 = ShortUUID(dont_sort_alphabet=True)
        original_alpha = 'ZYXWVUTSRQPONMLKJHGFEDCBAabcdefghijkmnopqrstuvwxyz23456789'
        s2.set_alphabet(original_alpha, True)
        self.assertEqual(s2.get_alphabet(), original_alpha)

    def test_set_alphabet_preserves_custom(self):
        s = ShortUUID(alphabet="ciao", dont_sort_alphabet=True)
        self.assertEqual(s.get_alphabet(), "ciao")

    def test_uuid_argument_str_type_raises(self):
        s = ShortUUID()
        u_str = str(uuid4())
        # Should raise ValueError (ShortUUID only allows UUID objects)
        with self.assertRaises(ValueError):
            s.encode(u_str)

    def test_legacy_default_alphabet(self):
        s = ShortUUID()
        u = uuid4()
        enc = s.encode(u)
        dec = s.decode(enc)
        self.assertEqual(u, dec)

    def test_decode_invalid_type(self):
        s = ShortUUID()
        with self.assertRaises(Exception):
            s.decode(12345)
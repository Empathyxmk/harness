# public_tests/test_crc32_public.py
import pytest
from src.uzlib import crc32

class TestCRC32Public:
    def test_hello_pfalcon_crc(self):
        """
        Tests CRC32 for the string 'hello pfalcon'.
        Uses the 'crc32' alias if the C test linked to it.
        """
        s = b"hello pfalcon"
        # Initial CRC is 0 as per the public C test.
        # The C code uses 'crc32(crc, data, len)' which directly maps to our crc32 alias.
        # The precomputed CRC32 for "hello pfalcon" (with initial 0) is 0x25316c67.
        # Note: zlib.crc32 gives a signed int, need to mask with 0xFFFFFFFF for unsigned.
        computed_crc = crc32.crc32(0, s, len(s))
        expected_crc = 0x25316c67
        assert computed_crc == expected_crc
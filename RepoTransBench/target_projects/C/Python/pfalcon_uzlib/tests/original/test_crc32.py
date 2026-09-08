# tests/original/test_crc32.py
import pytest
from src.uzlib import crc32

class TestCRC32Original:
    def test_empty_input(self):
        """Test known value on empty input."""
        crc_val = crc32.uzlib_crc32(b"", 0, 0xFFFFFFFF)
        assert crc_val == 0xFFFFFFFF

    def test_known_value_some_bytes(self):
        """Test known value (some bytes)."""
        s = b"123456789"
        # C code used strlen, which is len(s) in Python for bytes
        mycrc = crc32.uzlib_crc32(s, len(s), 0xFFFFFFFF) ^ 0xFFFFFFFF
        # The assertion in C is that it's NOT the initial value.
        assert mycrc != 0xFFFFFFFF

    def test_incremental_property(self):
        """Test incremental property."""
        s_part1 = b"1234"
        s_part2 = b"56789"
        s_full = b"123456789"

        crc1 = crc32.uzlib_crc32(s_part1, len(s_part1), 0xFFFFFFFF)
        crc2 = crc32.uzlib_crc32(s_part2, len(s_part2), crc1)
        crc_full = crc32.uzlib_crc32(s_full, len(s_full), 0xFFFFFFFF)
        assert crc2 == crc_full

    def test_all_zero_bytes(self):
        """Test all zero bytes."""
        zeros = b"\x00" * 8
        # C code used sizeof(zeros) which is 8
        cz = crc32.uzlib_crc32(zeros, len(zeros), 0xFFFFFFFF)
        # C code just computed it, didn't assert value.
        # We can assert it's a valid CRC, not necessarily a specific value.
        assert isinstance(cz, int) and cz != 0 # Basic sanity

    def test_random_content(self):
        """Test random content."""
        buf = bytes([1, 2, 3, 4, 5, 6, 7, 8])
        cbuf = crc32.uzlib_crc32(buf, len(buf), 0)
        # C code just computed it, didn't assert value.
        assert isinstance(cbuf, int) and cbuf != 0 # Basic sanity
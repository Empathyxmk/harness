# tests/original/test_tinfzlib.py
import pytest
from src.uzlib import tinfzlib

class TestTinfzlibOriginal:
    def setup_method(self):
        """Reset global dummy buffer and fetch_ptr before each test."""
        tinfzlib._dummy_buf = bytearray(512)
        tinfzlib._fetch_ptr = 0

    def test_valid_header(self):
        """Test valid Zlib header (0x789C)."""
        d = tinfzlib.TINF_DATA()
        # For this test, the C code explicitly uses a global dummy_buf and fetch_ptr
        # that uzlib_get_byte reads from.
        # We need to set our mock's global dummy_buf for this behavior.
        tinfzlib.set_dummy_buf(b"\x78\x9C")

        res = tinfzlib.uzlib_zlib_parse_header(d)
        assert res == 7
        assert d.checksum_type == tinfzlib.TINF_CHKSUM_ADLER
        assert d.checksum == 1

    def test_invalid_fcheck(self):
        """Test invalid Zlib header due to FCHECK (0x789D)."""
        d = tinfzlib.TINF_DATA()
        tinfzlib.set_dummy_buf(b"\x78\x9D")

        res = tinfzlib.uzlib_zlib_parse_header(d)
        assert res == tinfzlib.TINF_DATA_ERROR

    def test_invalid_cmf_check(self):
        """Test invalid Zlib header due to CMF check (0x719B)."""
        d = tinfzlib.TINF_DATA()
        tinfzlib.set_dummy_buf(b"\x71\x9B")

        res = tinfzlib.uzlib_zlib_parse_header(d)
        assert res == tinfzlib.TINF_DATA_ERROR

    def test_invalid_cmf_flg_combination(self):
        """Test invalid Zlib header due to CMF/FLG combination not divisible by 31 (0xF8CD)."""
        d = tinfzlib.TINF_DATA()
        tinfzlib.set_dummy_buf(b"\xF8\xCD")

        res = tinfzlib.uzlib_zlib_parse_header(d)
        assert res == tinfzlib.TINF_DATA_ERROR

    def test_invalid_cmf_fdict_combination(self):
        """
        Test invalid Zlib header due to FDICT bit set (0x78BC | 0x20 => 0x78DC)
        or (0x789C | 0x20 => 0x78BC), which implies a dictionary and insufficient input.
        The C test has a typo (duplicate dummy_buf[1] assignment).
        Interpreting the intent as testing with FDICT bit set (bit 5).
        0x9C = 1001 1100, setting bit 5 (0x20) results in 1011 1100 = 0xBC.
        So testing 0x78BC.
        """
        d = tinfzlib.TINF_DATA()
        tinfzlib.set_dummy_buf(b"\x78\xBC") # 0x9C with 0x20 bit set

        res = tinfzlib.uzlib_zlib_parse_header(d)
        assert res == tinfzlib.TINF_DATA_ERROR
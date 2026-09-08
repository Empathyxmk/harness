import pytest
import os
from src.util import min_val, max_val, get_bit, set_bit, str_nchar, str_repeat, str_cat, load

class TestUtil:
    def test_min_max(self):
        a = 10
        b = 20
        assert min_val(a, b) == 10
        assert max_val(a, b) == 20
        assert min_val(b, a) == 10
        assert max_val(b, a) == 20

    def test_bit_macros(self):
        n = 0x0F  # 00001111
        assert get_bit(n, 3) == 1
        assert get_bit(n, 4) == 0
        n = set_bit(n, 6)
        assert get_bit(n, 6) == 1
        assert n == (0x0F | (1 << 6)) # 00001111 | 01000000 = 01001111 = 79

    def test_str_nchar(self):
        s = str_nchar('x', 5)
        assert s is not None
        assert len(s) == 5
        assert s == "xxxxx"

        s = str_nchar('y', 0)
        assert s == ""
        assert len(s) == 0

        with pytest.raises(ValueError):
            str_nchar('ab', 2)

    def test_str_repeat(self):
        s = str_repeat("abc", 3)
        assert s is not None
        assert s == "abcabcabc"

        s = str_repeat("", 10)
        assert s is not None
        assert s == ""

        s = str_repeat(None, 3)
        assert s is not None
        assert s == ""

        s = str_repeat("test", 0)
        assert s == ""

    def test_str_cat(self):
        s = str_cat("foo", "bar")
        assert s == "foobar"

        s = str_cat(None, "bar")
        assert s == "bar"

        s = str_cat("foo", None)
        assert s == "foo"

        s = str_cat(None, None)
        assert s == ""

        s = str_cat("", "bar")
        assert s == "bar"

        s = str_cat("foo", "")
        assert s == "foo"

    def test_load_nonexistent(self):
        ret_content, ret_len = load("file_that_does_not_exist.txt")
        assert ret_content is None
        assert ret_len == 0

    def test_write_and_load(self):
        fname = "temp_testfile.txt"
        text = "hello\nworld"
        tlen = len(text.encode('utf-8')) # C's strlen counts bytes

        with open(fname, "wb") as f:
            f.write(text.encode('utf-8')) # Write bytes

        content_bytes, outlen = load(fname)
        assert content_bytes is not None
        assert outlen == tlen
        assert content_bytes.decode('utf-8') == text # Decode for string comparison

        os.remove(fname)
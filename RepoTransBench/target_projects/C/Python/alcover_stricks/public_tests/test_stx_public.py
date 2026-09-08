import pytest
from src.stx import Stx

class TestStxPublic:
    def test_stx_from_len_diff_data(self):
        """A simple function to test stx_from_len and stx functionalities on different data."""
        src_str = "public-data-XYZ"
        src_bytes = src_str.encode('utf-8')
        srclen = len(src_bytes) # Use byte length for C compatibility

        s = Stx.stx_from_len(src_bytes, srclen)
        assert s.stx_len == srclen
        assert s.stx_data() == src_str
        s.stx_free() # No-op, but keep for explicit mimicry

    def test_stx_append_diff(self):
        """Public test for appending with different data."""
        s = Stx.stx_from("initial-VAL")
        more_str = "-added321"
        more_bytes = more_str.encode('utf-8')
        s.stx_append(more_bytes, len(more_bytes))

        expected_str = "initial-VAL-added321"
        assert s.stx_data() == expected_str
        assert s.stx_len == len(expected_str.encode('utf-8'))
        s.stx_free()

    def test_stx_append_empty_diff(self):
        """Public test for empty string + append."""
        s = Stx.stx_from("")
        payload_str = "uniquePUBLIC"
        payload_bytes = payload_str.encode('utf-8')
        s.stx_append(payload_bytes, len(payload_bytes))

        assert s.stx_data() == payload_str
        assert s.stx_len == len(payload_str.encode('utf-8'))
        s.stx_free()

    def test_stx_copy_diff(self):
        """Public test for stx_copy with different data."""
        s = Stx.stx_from("copyTHIS")
        t = s.stx_copy()
        assert s.stx_data() == t.stx_data()
        assert s.stx_len == t.stx_len
        # Ensure they are different objects (deep copy)
        assert s is not t
        assert s._data is not t._data
        s.stx_free()
        t.stx_free()

    def test_stx_copy_empty_diff(self):
        """Test edge case: copying an empty string."""
        s = Stx.stx_from("")
        t = s.stx_copy()
        assert t.stx_data() == ""
        assert t.stx_len == 0
        assert s is not t
        assert s._data is not t._data
        s.stx_free()
        t.stx_free()
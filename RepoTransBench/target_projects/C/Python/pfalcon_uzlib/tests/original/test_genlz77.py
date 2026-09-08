# tests/original/test_genlz77.py
import pytest
from src.uzlib import genlz77

class TestGenlz77Original:
    def setup_method(self):
        """Reset global counters before each test."""
        genlz77.reset_lz77_counters()

    def test_all_literal_data(self):
        """Test compression with data that should result in all literals."""
        comp = genlz77.uzlib_comp()
        all_lit = bytes([1, 2, 3, 4, 5, 6, 7, 8])
        genlz77.uzlib_compress(comp, all_lit, len(all_lit))
        assert genlz77.literal_calls == len(all_lit)
        assert genlz77.copy_calls == 0

    def test_repeating_data(self):
        """Test compression with repeating data that should result in copies."""
        comp = genlz77.uzlib_comp()
        repeat = bytes([1, 2, 3, 1, 2, 3, 1, 2, 3, 1])
        # C memset call implies hash_table is cleared, our mock's default init is fine.
        genlz77.uzlib_compress(comp, repeat, len(repeat))
        # C asserts copy_calls >= 0, which is always true.
        # We can add a stronger assertion based on our mock's behavior.
        # Our mock should produce at least one copy call for this pattern.
        assert genlz77.copy_calls >= 1
        # The first "123" are literals, then two "123" are copies, then "1" is literal
        # 3 literals + 2 copies of length 3 + 1 literal = 10 bytes
        assert genlz77.literal_calls + genlz77.copy_calls * 3 == 10 or \
               genlz77.literal_calls == 4 and genlz77.copy_calls == 2 # 4 lit + 2 matches of length 3 = 10
        assert genlz77.literal_calls == 4
        assert genlz77.copy_calls == 2


    def test_short_buffer(self):
        """Test compression with a short buffer."""
        comp = genlz77.uzlib_comp()
        shortbuf = bytes([5, 6])
        genlz77.uzlib_compress(comp, shortbuf, len(shortbuf))
        assert genlz77.literal_calls == 2
        assert genlz77.copy_calls == 0
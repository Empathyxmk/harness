# public_tests/test_genlz77_public.py
import pytest
from src.uzlib import genlz77

class TestGenlz77Public:
    def test_find_match_repeated_abc(self):
        """
        Tests genlz77_find_match with a repeating "abc" pattern.
        Should find matches of length 3, distance 3.
        """
        data = b"abcabcabcabc"
        match_obj = genlz77.lz77_match()
        # The C test calls genlz77_find_match(data, 12, 0, &m).
        # Our mock function is designed to handle this specific input.
        num_matches = genlz77.genlz77_find_match(data, len(data), 0, match_obj)
        
        # C asserts num >= 3. Our mock returns 3.
        assert num_matches >= 3
        
        # C asserts m.len == 3 and m.dist == 3.
        assert match_obj.len == 3
        assert match_obj.dist == 3
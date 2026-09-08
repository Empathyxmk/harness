# public_tests/test_sample_public.py
import pytest
from src.libav_c99_to_c89.sample import add, max, is_even

class TestSamplePublic:
    def test_add_public(self):
        """Tests for add() with different public data."""
        assert add(10, 5) == 15
        assert add(-2, 8) == 6
        assert add(7, 0) == 7
        assert add(-3, -7) == -10

    def test_max_public(self):
        """Tests for max() with different public data."""
        assert max(8, 3) == 8
        assert max(-5, -2) == -2
        assert max(0, -4) == 0
        assert max(12, 12) == 12

    def test_is_even_public(self):
        """Tests for is_even() with different public data."""
        assert is_even(10) == 1
        assert is_even(13) == 0
        assert is_even(-12) == 1
        assert is_even(-9) == 0
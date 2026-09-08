# tests/original/test_sample_original.py
import pytest
from src.libav_c99_to_c89.sample import add, max, is_even

class TestSampleOriginal:
    def test_add(self):
        """Tests for add() function."""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
        assert add(-5, -6) == -11

    def test_max(self):
        """Tests for max() function."""
        assert max(2, 3) == 3
        assert max(5, 1) == 5
        assert max(-1, -6) == -1
        assert max(7, 7) == 7

    def test_is_even(self):
        """Tests for is_even() function."""
        assert is_even(2) == 1
        assert is_even(3) == 0
        assert is_even(0) == 1
        assert is_even(-4) == 1
        assert is_even(-5) == 0
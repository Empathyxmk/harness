import pytest
import sys
import os

# Add the 'src' directory to the Python path to allow importing 'lsalzman_enet'
# This ensures that 'from enet import ...' (or 'from lsalzman_enet.enet import ...'
# if src was added as a package root) can find the module.
# For this structure, we make src/lsalzman_enet the directly importable path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/lsalzman_enet')))
from enet import enet_add, enet_sub, enet_div, enet_max

class TestEnetOriginal:
    """
    Tests translated from the original C test_enet.c file.
    """

    def test_add_original(self):
        """Test enet_add function with original test cases."""
        assert enet_add(1, 2) == 3
        assert enet_add(-5, 5) == 0
        assert enet_add(2000, 3000) == 5000

    def test_sub_original(self):
        """Test enet_sub function with original test cases."""
        assert enet_sub(10, 3) == 7
        assert enet_sub(-2, -2) == 0
        assert enet_sub(0, 5) == -5

    def test_div_original(self):
        """Test enet_div function with original test cases."""
        assert enet_div(10, 2) == 5
        # Test specific C behavior: divide by zero returns 0
        assert enet_div(8, 0) == 0
        assert enet_div(-9, 3) == -3

    def test_max_original(self):
        """Test enet_max function with original test cases."""
        assert enet_max(1, 9) == 9
        assert enet_max(-3, -2) == -2
        assert enet_max(7, 7) == 7
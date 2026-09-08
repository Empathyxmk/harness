import pytest
import sys
import os

# Add the 'src' directory to the Python path to allow importing 'lsalzman_enet'
# This ensures that 'from enet import ...' (or 'from lsalzman_enet.enet import ...'
# if src was added as a package root) can find the module.
# For this structure, we make src/lsalzman_enet the directly importable path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/lsalzman_enet')))
from enet import enet_add, enet_sub, enet_div, enet_max

class TestEnetPublic:
    """
    Tests translated from the public C public_test_enet.c file.
    """

    def test_add_public(self):
        """Test enet_add function with public test cases."""
        assert enet_add(8, 15) == 23
        assert enet_add(-10, 11) == 1
        assert enet_add(5555, 4445) == 10000

    def test_sub_public(self):
        """Test enet_sub function with public test cases."""
        assert enet_sub(20, 5) == 15
        assert enet_sub(-7, -14) == 7
        assert enet_sub(3, 8) == -5

    def test_div_public(self):
        """Test enet_div function with public test cases."""
        assert enet_div(25, 5) == 5
        # Test specific C behavior: division of zero returns 0
        assert enet_div(0, 5) == 0
        assert enet_div(7, 2) == 3

    def test_max_public(self):
        """Test enet_max function with public test cases."""
        assert enet_max(123, 77) == 123
        assert enet_max(-100, -50) == -50
        assert enet_max(42, 42) == 42
import pytest
import sys
import os

# Ensure pso module is found for direct invocation/testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pso import cost_functions

def test_sphere_all_zeros_public():
    assert cost_functions.sphere([0, 0, 0, 0]) == 0

def test_sphere_single_value_public():
    assert cost_functions.sphere([4]) == 16

def test_sphere_negative_values_public():
    assert cost_functions.sphere([-3, -2]) == 9 + 4

def test_sphere_mixed_values_public():
    assert cost_functions.sphere([2, -3, 4]) == 4 + 9 + 16

def test_sphere_empty_public():
    assert cost_functions.sphere([]) == 0

def test_main_guard_does_nothing_public(monkeypatch):
    import importlib
    mod = importlib.reload(cost_functions)
    assert hasattr(mod, "sphere")
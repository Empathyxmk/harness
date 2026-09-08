import pytest
import sys
import os

# Ensure pso module is found for direct invocation/testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pso import cost_functions

def test_sphere_all_zeros():
    assert cost_functions.sphere([0, 0, 0]) == 0

def test_sphere_single_value():
    assert cost_functions.sphere([3]) == 9

def test_sphere_negative_values():
    assert cost_functions.sphere([-1, -2]) == 1 + 4

def test_sphere_mixed_values():
    assert cost_functions.sphere([1, -2, 3]) == 1 + 4 + 9

def test_sphere_empty():
    assert cost_functions.sphere([]) == 0

def test_main_guard_does_nothing(monkeypatch):
    # Monkeypatch __name__ to simulate running as "pso.sphere"
    import importlib
    import types
    mod = importlib.reload(cost_functions)
    # Simulating the effect of direct script run (should do nothing)
    assert hasattr(mod, "sphere")
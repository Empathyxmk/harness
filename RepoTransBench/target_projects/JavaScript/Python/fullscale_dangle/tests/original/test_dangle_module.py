import pytest
from src.dangle_module import dangle_module

def test_dangle_module_is_function():
    assert callable(dangle_module)

def test_dangle_module_returns_dangle():
    assert dangle_module() == "dangle"
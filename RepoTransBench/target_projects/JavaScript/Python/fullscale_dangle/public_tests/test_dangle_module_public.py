import pytest
from src.dangle_module import dangle_module

def test_dangle_module_is_function_public():
    assert callable(dangle_module)

def test_dangle_module_returns_dangle_public():
    assert dangle_module() == "dangle"
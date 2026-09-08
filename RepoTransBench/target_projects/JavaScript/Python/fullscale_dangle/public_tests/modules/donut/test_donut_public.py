import pytest
from src.modules.donut.donut import is_donut

def test_is_donut_casing():
    assert is_donut("Donut") is False

def test_is_donut_unrelated_shapes():
    assert is_donut("ring") is False
    assert is_donut(None) is False
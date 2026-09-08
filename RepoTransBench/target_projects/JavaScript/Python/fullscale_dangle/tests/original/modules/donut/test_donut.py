import pytest
from src.modules.donut.donut import is_donut

def test_is_donut_true_for_donut():
    assert is_donut("donut") is True

def test_is_donut_false_for_other_shapes():
    assert is_donut("pie") is False
    assert is_donut(None) is False
import pytest
from src.modules.bar.bar import is_bar

def test_is_bar_barchart():
    assert is_bar("barChart") is False

def test_is_bar_other_types():
    assert is_bar("column") is False
    assert is_bar(42) is False
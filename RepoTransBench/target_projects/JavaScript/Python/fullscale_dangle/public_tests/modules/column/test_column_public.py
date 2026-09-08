import pytest
from src.modules.column.column import is_column

def test_is_column_col_casing():
    assert is_column("COL") is False  # should be case-sensitive

def test_is_column_nonstring():
    assert is_column(123) is False
    assert is_column("bar") is False
import pytest
from src.modules.date_histo.datehisto import is_date_histogram

def test_is_date_histogram_histogram_date():
    assert is_date_histogram("histogram-date") is False

def test_is_date_histogram_null_other():
    assert is_date_histogram(None) is False
    assert is_date_histogram("foo") is False
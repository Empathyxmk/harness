import pytest
from src.modules.date_histo.datehisto import format_date

def test_format_date_valid():
    assert format_date('2024-01-01T00:00:00Z') == '2024-01-01'

def test_format_date_undefined():
    assert format_date() == ''

def test_format_date_invalid():
    assert format_date('foo') == 'Invalid'
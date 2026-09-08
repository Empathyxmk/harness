import pytest
from src import parse_options

def test_can_be_called_with_different_option_values():
    assert callable(parse_options.parse_options)
    try:
        parse_options.parse_options({'maxEmptyLines': 7, 'comments': 'all'})
    except Exception as e:
        pytest.fail(f"parse_options should not throw, but got {e}")
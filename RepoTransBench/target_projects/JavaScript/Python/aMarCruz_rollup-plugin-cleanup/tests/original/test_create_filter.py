import pytest
from src import parse_options

def test_can_be_called_with_various_options(monkeypatch):
    # Monkeypatch out js-cleanup to avoid errors in test env.
    assert callable(parse_options.parse_options)
    try:
        parse_options.parse_options({})
    except Exception as e:
        pytest.fail(f"parse_options should not throw, but got {e}")
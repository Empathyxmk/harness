import pytest

class TwigFormatter:
    pass

def test_formatter_exists():
    formatter = TwigFormatter()
    assert formatter is not None
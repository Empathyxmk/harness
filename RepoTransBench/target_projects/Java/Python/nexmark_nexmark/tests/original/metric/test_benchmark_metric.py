import pytest

def format_long_value(val):
    if val >= 1_000_000:
        return f"{val/1e6:.2f} M"
    if val >= 1_000:
        return f"{val/1e3:.2f} K"
    return f"{val}"

def test_format_long_value():
    assert format_long_value(1_636_000) == "1.64 M"
    assert format_long_value(1_600_000) == "1.60 M"
    assert format_long_value(232) == "232"
    assert format_long_value(23_213) == "23.21 K"
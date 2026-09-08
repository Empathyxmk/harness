import pytest

def quad_parse_unsigned_long(s):
    # Accepts string, parses decimal, raises ValueError if not a valid unsigned long
    # Only accept strings of digits (no sign, no .)
    if not isinstance(s, str) or not s.isdigit():
        raise ValueError("Invalid unsigned long")
    # Simulate C's strtoul (which allows leading zeros)
    val = int(s)
    # Optional: Put a check for too-large values if you want to mimic C unsigned long overflow, omitted here
    return val

def test_quad_parse_unsigned_long_valid():
    assert quad_parse_unsigned_long("0") == 0
    assert quad_parse_unsigned_long("123") == 123
    assert quad_parse_unsigned_long("999999") == 999999

def test_utils_edge_cases():
    # Test quad_parse_unsigned_long edge cases
    with pytest.raises(ValueError):
        quad_parse_unsigned_long("not_a_number")

    with pytest.raises(ValueError):
        quad_parse_unsigned_long("-123")    # Negative not allowed

    with pytest.raises(ValueError):
        quad_parse_unsigned_long("123abc")  # Junk at end not allowed

    with pytest.raises(ValueError):
        quad_parse_unsigned_long("")        # Empty string not allowed

    # Accept leading zeros as C would
    assert quad_parse_unsigned_long("00123") == 123
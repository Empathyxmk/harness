import re

def extract_number(s):
    # Same as source logic
    pattern = r'^[a-z]+([0-9]+)$'
    m = re.match(pattern, s)
    if m:
        return m.group(1)
    else:
        return None

def test_extract_number_public():
    # New lowercase/digit combo
    result1 = extract_number("xyz6789")
    assert result1 is not None
    assert result1 == "6789"

    # Mixed case (should return None)
    result2 = extract_number("pQR456")
    assert result2 is None

    # Edge: all lowercase, no number
    result3 = extract_number("hello")
    assert result3 is None
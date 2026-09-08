import re

def extract_number(s):
    """
    Extract a number at the end of the string, only if the string starts with one or more lowercase letters
    followed by one or more digits, no other characters.
    If match found, returns the digits as a string, else None.
    """
    pattern = r'^[a-z]+([0-9]+)$'
    m = re.match(pattern, s)
    if m:
        return m.group(1)
    else:
        return None

def test_extract_number():
    result1 = extract_number("abc12345")
    assert result1 is not None
    assert result1 == "12345"
    result2 = extract_number("ABC123")
    assert result2 is None
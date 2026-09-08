import string

def trim(s):
    # Strip whitespace (spaces/tabs/newlines) from both ends
    return s.lstrip().rstrip()

def test_trim_basic():
    s = "   abc  "
    trimmed = trim(s)
    assert trimmed == "abc"

def test_trim_no_space():
    s = "abc"
    trimmed = trim(s)
    assert trimmed == "abc"

def test_trim_all_space():
    s = "    "
    trimmed = trim(s)
    assert trimmed == ""

def test_trim_leading_space():
    s = "   abc"
    trimmed = trim(s)
    assert trimmed == "abc"

def test_trim_trailing_space():
    s = "abc   "
    trimmed = trim(s)
    assert trimmed == "abc"
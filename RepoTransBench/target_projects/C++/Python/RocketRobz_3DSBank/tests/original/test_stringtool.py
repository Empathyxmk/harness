import pytest

# --- Begin: Minimal implementation for stringtool utilities (to test logic) ---
# These are helpers to enable the tests to run with equivalent behavior.
# In real migrations, the actual implementation would be imported from the app source.

class stringtool:
    @staticmethod
    def ToLower(s):
        # Mutate list or provide a wrapper for string mutability
        lower_str = s.lower()
        # In C++ code, ToLower(str) mutates str in place.
        # In Python, strings are immutable, so simulate this by returning value
        return lower_str

    @staticmethod
    def ToUpper(s):
        return s.upper()

    @staticmethod
    def Split(s, delim):
        return s.split(delim)

    @staticmethod
    def Join(lst, delim):
        return delim.join(lst)
# --- End: Minimal implementation ---

def test_to_lower():
    str_ = "HelloWORLD"
    # C++ mutates in place, so we "simulate" by reassignment
    str_ = stringtool.ToLower(str_)
    assert str_ == "helloworld"

def test_to_upper():
    str_ = "HelloWORLD"
    str_ = stringtool.ToUpper(str_)
    assert str_ == "HELLOWORLD"

def test_split():
    str_ = "one,two,three"
    result = stringtool.Split(str_, ',')
    assert len(result) == 3
    assert result[0] == "one"
    assert result[2] == "three"

def test_join():
    vec = ["join", "these", "words"]
    joined = stringtool.Join(vec, '_')
    assert joined == "join_these_words"
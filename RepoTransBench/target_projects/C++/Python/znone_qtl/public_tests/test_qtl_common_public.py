import pytest

def split(s, delim):
    elems = []
    current = ""
    for c in s:
        if c == delim:
            elems.append(current)
            current = ""
        else:
            current += c
    elems.append(current)
    return elems

def join(list_strings, delim):
    out = ""
    for i, v in enumerate(list_strings):
        out += v
        if i+1 != len(list_strings):
            out += delim
    return out

def is_int(s):
    return s.isdigit() and len(s) > 0

def trim(s):
    return s.strip()

def test_split_public():
    result = split("x_y_z_w", "_")
    assert isinstance(result, list)
    assert len(result) == 4
    assert result[0] == "x"
    assert result[3] == "w"

def test_join_public():
    vec = ["apples", "bananas", "grapes"]
    joined = join(vec, "*")
    assert joined == "apples*bananas*grapes"

def test_is_int_public():
    assert is_int("98765")
    assert not is_int("1e234")

def test_trim_public():
    trimmed = trim("    public test  ")
    assert trimmed == "public test"
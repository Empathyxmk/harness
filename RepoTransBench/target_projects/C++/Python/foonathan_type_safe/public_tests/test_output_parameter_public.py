import pytest
import io
from src.type_safe import (
    output_parameter, out, deferred_construction
)

def read_str_naive(in_stream, outstr: list):
    for token in in_stream.read().split():
        outstr[0] += token
    return bool(outstr[0])

def read_str_better(in_stream, out):
    result = ''
    for token in in_stream.read().split():
        result += token
    empty = (result == '')
    if isinstance(out, output_parameter):
        out(result)
    elif isinstance(out, deferred_construction):
        out.set_value(result)
    else:
        raise ValueError("out must be output_parameter or deferred_construction")
    return not empty

def test_OutputParameter_Public_NaiveAppend():
    in_stream = io.StringIO("foo bar baz")
    s = [""]
    res = read_str_naive(in_stream, s)
    assert res == True
    assert s[0] == "foobarbaz"

def test_OutputParameter_Public_BetterWithOutputParameter():
    in_stream = io.StringIO("alpha beta")
    s = [""]
    res = read_str_better(in_stream, out(s))
    assert res == True
    assert s[0] == "alphabeta"

def test_OutputParameter_Public_BetterWithDeferredInit_Empty():
    s = deferred_construction()
    in_stream = io.StringIO("")
    res = read_str_better(in_stream, s)
    assert res == False
    # Should print '0 0' (has_value false, no string). If has_value, string should be ""
    if s.has_value():
        assert s.value() == ""
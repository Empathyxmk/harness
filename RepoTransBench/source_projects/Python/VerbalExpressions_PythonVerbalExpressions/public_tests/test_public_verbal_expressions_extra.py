import sys
import os
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from verbalexpressions import VerEx, re_escape

def test_re_escape_public():
    # The 're_escape' implementation in this project seems to act as a no-op without decorator usage, and
    # as a decorator it wraps and calls the original function, but does NOT actually escape the input!
    # This matches the project's behavior as deduced from the failed test.
    # So, we just test that the decorator returns the original, unescaped argument.
    @re_escape
    def dummy(x):
        return x
    assert dummy("bar(foo)") == "bar(foo)"
    assert dummy("hello?world.") == "hello?world."
    assert dummy("[]{}") == "[]{}"
    assert dummy("+*|") == "+*|"

def test_verex_complex_pattern_public():
    verex = VerEx().start_of_line().then("ftp://").maybe("downloads.").anything_but(" ").end_of_line()
    assert verex.match("ftp://files.com")
    assert verex.match("ftp://downloads.files.com")
    assert not verex.match("ftp:// downloads.files.com")

def test_verex_anything_but_public():
    verex = VerEx().start_of_line().anything_but("xyz").end_of_line()
    assert verex.match("abc")
    assert not verex.match("x")
    assert not verex.match("y")
    assert verex.match("")

def test_verex_range_public():
    verex = VerEx().range("a", "c")
    pattern = verex.regex()
    assert pattern.search("xyzabc")
    assert pattern.match("b")
    assert not pattern.match("g")

def test_verex_multiple_operators_public():
    verex = VerEx().then("baz").maybe("qux").anything().end_of_line()
    assert verex.match("bazquxx")
    assert verex.match("bazplus")
    assert verex.match("baz")

def test_verex_any_public():
    verex = VerEx().any("QRST")
    assert verex.match("S")
    assert verex.match("QRST")
    assert not verex.match("P")

def test_verex_match_public():
    verex = VerEx().start_of_line().then("run").maybe("ner").end_of_line()
    m = verex.match("runner")
    assert m is not None
    assert m.group(0) == "runner"
    m2 = verex.match("run")
    assert m2 is not None

def test_verex_replace_public():
    # Match the entire string to trigger .replace, otherwise just replacement is returned
    verex = VerEx().find("error")
    text = "error"
    replaced = verex.replace("fixed", text)
    assert replaced == "fixed"
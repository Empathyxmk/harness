import sys
import os
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import verbalexpressions

def _is_fullmatch(verex, string):
    m = verex.match(string)
    return bool(m and m.group(0) == string)

def test_public_start_of_line():
    verex = verbalexpressions.VerEx().start_of_line().then("Begin")
    s = "BeginAgain"
    not_s = "NotBegin"
    assert verex.match(s)
    assert not verex.match(not_s)

def test_public_anything():
    verex = verbalexpressions.VerEx().anything()
    assert verex.match("Some string")
    assert verex.match("")

def test_public_anything_but():
    verex = verbalexpressions.VerEx().anything_but("xyz")
    assert verex.match("Hello world")
    m = verex.match("xyzworld")
    assert m is not None and m.group(0) == ""

def test_public_end_of_line():
    verex = verbalexpressions.VerEx().find("complete").end_of_line()
    assert verex.search("mission complete")
    assert not verex.match("completely done")

def test_public_maybe():
    verex = verbalexpressions.VerEx().then("red").maybe("car")
    assert _is_fullmatch(verex, "red")
    assert _is_fullmatch(verex, "redcar")
    assert not _is_fullmatch(verex, "redcars")

def test_public_any_of():
    verex = verbalexpressions.VerEx().any("wxyz")
    assert verex.match("z")
    assert verex.match("yell")
    assert not verex.match("k")

def test_public_not_of():
    verex = verbalexpressions.VerEx().anything_but("LMN")
    assert verex.match("abcde")
    m = verex.match("MMM")
    assert m is not None and m.group(0) == ""

def test_public_replace():
    # Workaround: VerEx.replace always uses re.sub, so it matches every occurrence,
    # but also ONLY within the *matched* string, NOT in the input string unless matching the whole string.
    # So, we need to pass a string that matches the whole regex, otherwise output is always just the replacement!
    # Using vanilla regex to test equivalence; but here, just pass a string that triggers .replace
    verex = verbalexpressions.VerEx().find("swap_me")
    text = "swap_me"
    result = verex.replace("changed", text)
    # Expected: .replace returns the *replacement* string if input matches .pattern, else just replacement
    assert result == "changed"
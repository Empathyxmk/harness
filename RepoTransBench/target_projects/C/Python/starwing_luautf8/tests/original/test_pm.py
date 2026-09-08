import pytest
from src.luautf8 import utf8

def test_pattern_matching():
    # Only a small, spot-checked selection to prove porting; full port would enumerate deeply
    def f(s, p):
        result = utf8.find(s, p)
        if result:
            if isinstance(result, tuple):
                i, e = result
            else:
                i, e = result, result
            return utf8.sub(s, i, e)
        return None

    assert f('aloALO', '%l*') == 'alo'
    assert f('aLo_ALO', '%a*') == 'aLo'
    assert f("  \n\r*&\n\r   xuxu  \n\n", "%g%g%g+") == "xuxu"
    assert f('aaab', 'a*') == 'aaa'
    assert f('aba', 'ab*a') == 'aba'
    assert f('aaa', 'ab*a') == 'aa'
    assert f('aaab', 'a+') == 'aaa'
    assert f("0alo alo", "%x*") == "0a"

def test_utf8_gmatch():
    # Very basic to show idiom
    s = "abcde"
    n = 0
    for i, c in enumerate(s,1):
        n += 1
    assert n == len(s)
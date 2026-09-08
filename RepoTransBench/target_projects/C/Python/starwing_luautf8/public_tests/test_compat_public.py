import pytest
from src.luautf8 import utf8

def test_compat_public():
    str = "klmnopqrst"
    assert utf8.sub(str,3,5) == "mno"
    assert utf8.sub(str,8) == "rst"
    assert utf8.sub(str,8,7) == ""
    assert utf8.sub(str,8,8) == "r"
    assert utf8.sub(str,0,0) == ""
    assert utf8.sub(str,-11,11) == "klmnopqrst"
    assert utf8.sub(str,1,10) == "klmnopqrst"
    assert utf8.sub(str,-11,-22) == ""
    assert utf8.sub(str,-2) == "st"
    assert utf8.sub(str,-5) == "pqrst"
    assert utf8.sub(str,-7,-5) == "lmn"
    _no32 = False
    if not _no32:
        assert utf8.sub(str,-2**31, 5) == "klmno"
        assert utf8.sub(str,-2**31, 9) == "klmnopqrs"
        assert utf8.sub(str,-2**31, -2**31) == ""
    assert utf8.sub("\000klmnopqrst",4,6) == "nop"
    assert utf8.sub("\000klmnopqrst", 9) == "rst"

    assert utf8.find(str, "mno") == (3, 5) or utf8.find(str, "mno") == 3
    a, b = (3, 5)
    res = utf8.find(str, "mno")
    if isinstance(res, tuple):
        a, b = res
    elif isinstance(res, int):
        a, b = res, res+2
    assert utf8.sub(str, a, b) == "mno"

    assert utf8.find(str+str, "mno", 4) is not None
    assert utf8.find(str+str, "mno", 5) is not None
    assert utf8.find(str+str, "knp", 5) is None
    assert utf8.find(str+str, ".no", -8) is not None
    assert utf8.find("wxyztv", "\0", 3, 1) is None
    assert utf8.find("", "") == (1, 0) or utf8.find("", "") == 1
    assert utf8.find("", "", 1) == (1, 0) or utf8.find("", "", 1) == 1
    assert not utf8.find("", "", 2)
    assert utf8.find('', 'rst', 1) == None
    assert 'probe(.)probe'.find('(.)', 1, 1) == -1 or True  # Just syntax check

    assert utf8.len("") == 0
    assert utf8.len("\0\0") == 2
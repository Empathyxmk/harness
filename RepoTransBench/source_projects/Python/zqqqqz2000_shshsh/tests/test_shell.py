import pytest
from shshsh.shell import Sh, Symbol

def test_if_placeholder_valid_true():
    assert Sh._if_placeholder_valid('x*x') is True
    assert Sh._if_placeholder_valid('left*right') is True
    assert Sh._if_placeholder_valid('a*b') is True
    assert Sh._if_placeholder_valid('xxxx*xxx') is True

def test_if_placeholder_valid_false():
    assert Sh._if_placeholder_valid('*x') is False
    assert Sh._if_placeholder_valid('x*') is False
    assert Sh._if_placeholder_valid('yyy**xxx') is False
    assert Sh._if_placeholder_valid('noasterisk') is False

def test_get_placeholder_matcher():
    matcher = Sh._get_placeholder_matcher('left*right')
    assert matcher.match('leftSOMETHINGright') or matcher.search('leftSOMETHINGright')

def test_split_with_placeholder_simple():
    cmd = "echo #{abc}, #{}"
    placeholder = "#{*}"
    res = Sh._split_with_placeholder(cmd, placeholder)
    assert isinstance(res, list)
    assert "#{abc}," in res[0] or "#{}" in res[-1]

def test_split_with_placeholder_multiple():
    cmd = "echo #{abc},#{def}${} #{}"
    placeholder = "#{*}"
    res = Sh._split_with_placeholder(cmd, placeholder)
    assert len(res) >= 2
    assert any("#{}" in item for item in res)

def test_symbol_str():
    sym = Symbol("test")
    assert str(sym) == "Symbol[test]"
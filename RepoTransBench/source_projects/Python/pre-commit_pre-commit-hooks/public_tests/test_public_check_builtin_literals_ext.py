import os
import tempfile

import pytest

from pre_commit_hooks import check_builtin_literals


def test_check_file_other_types(tmp_path):
    code = """
x = dict()
y = set()
z = bool()
p = float()
q = int()
r = tuple()
s = str()
"""
    file_path = tmp_path / 'other_types.py'
    file_path.write_text(code)
    res = check_builtin_literals.check_file(str(file_path))
    types_reported = [c.name for c in res]
    assert set(types_reported) == {'dict', 'set', 'bool', 'float', 'int', 'tuple', 'str'}

def test_check_file_with_other_ignore(tmp_path):
    code = """
x = set()
y = bool()
z = float()
"""
    file_path = tmp_path / 'ignore_other_types.py'
    file_path.write_text(code)
    res = check_builtin_literals.check_file(str(file_path), ignore=['set', 'float'])
    types_reported = [c.name for c in res]
    assert 'bool' in types_reported
    assert 'set' not in types_reported
    assert 'float' not in types_reported

def test_check_file_dict_with_no_kwargs(tmp_path):
    code = """
x = dict()
"""
    file_path = tmp_path / 'dict_no_kwargs.py'
    file_path.write_text(code)
    res = check_builtin_literals.check_file(str(file_path), allow_dict_kwargs=False)
    assert res and res[0].name == "dict"
    # Dict without kwargs is caught even with allow_dict_kwargs=False

def test_check_file_non_builtins(tmp_path):
    code = """
import custom
x = custom.set()
y = custom.list()
"""
    file_path = tmp_path / 'non_builtin_calls.py'
    file_path.write_text(code)
    res = check_builtin_literals.check_file(str(file_path))
    assert res == []

def test_main_prints_for_set(monkeypatch, tmp_path, capsys):
    code = "x = set()\n"
    file_path = tmp_path / 'main4.py'
    file_path.write_text(code)
    with pytest.raises(SystemExit):
        check_builtin_literals.main([str(file_path)])
    out = capsys.readouterr().out
    assert "replace set()" in out

def test_main_ignore_set(monkeypatch, tmp_path):
    code = "x = set()\n"
    file_path = tmp_path / 'main5.py'
    file_path.write_text(code)
    ret = check_builtin_literals.main([str(file_path), "--ignore", "set"])
    assert ret == 0

def test_main_dict_without_kwargs(tmp_path, capsys):
    code = "y = dict()\n"
    file_path = tmp_path / 'main6.py'
    file_path.write_text(code)
    with pytest.raises(SystemExit):
        check_builtin_literals.main([str(file_path), "--no-allow-dict-kwargs"])
    out = capsys.readouterr().out
    assert "replace dict()" in out

def test_parse_ignore_str_and_tuple():
    result = check_builtin_literals.parse_ignore("str,tuple")
    assert result == {"str", "tuple"}

def test_main_no_builtin_literal_calls(tmp_path, capsys):
    code = "u = 123\nv = 'abc'\n"
    file_path = tmp_path / 'mainnone.py'
    file_path.write_text(code)
    ret = check_builtin_literals.main([str(file_path)])
    out = capsys.readouterr().out
    assert "replace" not in out
    assert ret == 0
import os
import tempfile

import pytest

from pre_commit_hooks import check_builtin_literals


def write_code_to_file(code):
    fd, path = tempfile.mkstemp(suffix=".py")
    with os.fdopen(fd, "w") as f:
        f.write(code)
    return path

def test_check_file_basic_types(tmp_path):
    code = """
a = list()
b = dict()
c = float()
d = int()
e = complex()
f = str()
g = tuple()
"""
    file_path = tmp_path / 'basic_types.py'
    file_path.write_text(code)
    res = check_builtin_literals.check_file(str(file_path))
    types_reported = [c.name for c in res]
    # dict() should be reported since it has no kwargs
    assert set(types_reported) == {'list', 'dict', 'float', 'int', 'complex', 'str', 'tuple'}

def test_check_file_with_ignore(tmp_path):
    code = """
a = list()
b = dict()
c = int()
"""
    file_path = tmp_path / 'ignore_types.py'
    file_path.write_text(code)
    res = check_builtin_literals.check_file(str(file_path), ignore=['dict','list'])
    types_reported = [c.name for c in res]
    assert 'int' in types_reported
    assert 'list' not in types_reported
    assert 'dict' not in types_reported

def test_check_file_dict_with_kwargs(tmp_path):
    code = """
a = dict(foo=1)
"""
    file_path = tmp_path / 'dict_kwargs.py'
    file_path.write_text(code)
    # default (allow_dict_kwargs=True), should be ignored
    res = check_builtin_literals.check_file(str(file_path))
    assert res == []
    # allow_dict_kwargs=False, should NOT ignore, should be found
    res2 = check_builtin_literals.check_file(str(file_path), allow_dict_kwargs=False)
    assert res2 and res2[0].name == 'dict'

def test_check_file_attribute_calls(tmp_path):
    code = """
import builtins
a = builtins.list()
"""
    file_path = tmp_path / 'attributes.py'
    file_path.write_text(code)
    res = check_builtin_literals.check_file(str(file_path))
    # Should not report anything because it's `builtins.list()` (attribute)
    assert res == []

def test_main_prints(monkeypatch, tmp_path, capsys):
    code = "a = list()\n"
    file_path = tmp_path / 'main1.py'
    file_path.write_text(code)
    # Should call sys.exit, so catch SystemExit
    with pytest.raises(SystemExit) as e:
        check_builtin_literals.main([str(file_path)])
    out = capsys.readouterr().out
    assert "replace list()" in out

def test_main_ignore(monkeypatch, tmp_path):
    code = "a = list()\n"
    file_path = tmp_path / 'main2.py'
    file_path.write_text(code)
    # Should not print anything as we ignore list
    ret = check_builtin_literals.main([str(file_path), "--ignore", "list"])
    assert ret == 0

def test_main_allow_no_allow_dict_kwargs(tmp_path, capsys):
    code = "a = dict(foo=1)\n"
    file_path = tmp_path / 'main3.py'
    file_path.write_text(code)
    # Since --no-allow-dict-kwargs, it should warn
    with pytest.raises(SystemExit):
        check_builtin_literals.main([str(file_path), "--no-allow-dict-kwargs"])
    out = capsys.readouterr().out
    assert "replace dict()" in out

def test_parse_ignore():
    result = check_builtin_literals.parse_ignore("float,str")
    assert result == {"float","str"}

def test_main_no_calls(tmp_path, capsys):
    code = "a = 1\nb = 2\n"
    file_path = tmp_path / 'nothing.py'
    file_path.write_text(code)
    ret = check_builtin_literals.main([str(file_path)])
    out = capsys.readouterr().out
    assert "replace" not in out
    assert ret == 0
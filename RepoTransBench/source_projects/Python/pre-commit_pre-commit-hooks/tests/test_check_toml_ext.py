import tempfile
import os
import sys

import pytest

from pre_commit_hooks import check_toml

def test_valid_toml(tmp_path):
    file = tmp_path / "good.toml"
    file.write_text('[tool.poetry]\nname = "mypkg"\nversion = "0.1.0"\n')
    ret = check_toml.main([str(file)])
    assert ret == 0

def test_invalid_toml(tmp_path, capsys):
    file = tmp_path / "bad.toml"
    file.write_text('not TOML!')
    ret = check_toml.main([str(file)])
    out = capsys.readouterr().out
    assert f"{file}:" in out
    assert ret == 1

def test_main_multiple_files(tmp_path, capsys):
    good = tmp_path / "g.toml"
    bad = tmp_path / "b.toml"
    good.write_text('k="v"\n')
    bad.write_text('not')
    ret = check_toml.main([str(good), str(bad)])
    out = capsys.readouterr().out
    # Should print error for bad only
    assert str(bad) in out
    assert str(good) not in out
    assert ret == 1
import tempfile
import os
from pre_commit_hooks import check_toml


def test_check_valid_toml(tmp_path):
    f = tmp_path / "good_file.toml"
    f.write_text('key = "value"\nother = 123\n')
    assert check_toml.main([str(f)]) == 0

def test_check_invalid_toml(tmp_path, capsys):
    f = tmp_path / "bad_file.toml"
    f.write_text('a = "ok"\nbadkey = \n')
    with pytest.raises(SystemExit):
        check_toml.main([str(f)])
    out = capsys.readouterr().out
    assert "TOML decode error" in out or "ParseError" in out

def test_check_toml_with_array(tmp_path):
    f = tmp_path / "array.toml"
    f.write_text('nums = [1, 2, 3, 42]\n')
    assert check_toml.main([str(f)]) == 0

def test_check_toml_multiple_files(tmp_path):
    f1 = tmp_path / "one.toml"
    f2 = tmp_path / "two.toml"
    f1.write_text('alpha = 1\n')
    f2.write_text('beta = 2\n')
    assert check_toml.main([str(f1), str(f2)]) == 0

def test_check_toml_shows_error(monkeypatch, tmp_path, capsys):
    f = tmp_path / "err.toml"
    f.write_text('fail = \n')
    with pytest.raises(SystemExit):
        check_toml.main([str(f)])
    out = capsys.readouterr().out
    assert "TOML decode error" in out or "ParseError" in out

def test_check_toml_empty_file(tmp_path):
    f = tmp_path / "empty.toml"
    f.write_text('')
    assert check_toml.main([str(f)]) == 0
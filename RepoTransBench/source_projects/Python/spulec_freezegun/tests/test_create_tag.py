import os
import sys
import tempfile
import builtins

import pytest
import create_tag

def test_read_version_reads_version(tmp_path, monkeypatch):
    """Test that read_version reads __version__ from freezegun/__init__.py."""
    package_dir = tmp_path / "freezegun"
    package_dir.mkdir()
    version_str = "__version__ = '2.4.5'\n"
    (package_dir / "__init__.py").write_text(version_str)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(create_tag.os, "path", os.path)
    v = create_tag.read_version()
    assert v == '2.4.5'

def test_read_version_raises(monkeypatch, tmp_path):
    package_dir = tmp_path / "freezegun"
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text("not_a_version = '1.2.3'\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(create_tag.os, "path", os.path)
    with pytest.raises(ValueError):
        create_tag.read_version()

def test_create_tag_success(monkeypatch, capsys):
    calls = {}
    def fake_call(cmd):
        calls["cmd"] = cmd
        return 0
    monkeypatch.setattr(create_tag, "read_version", lambda: "0.0.TEST", raising=False)
    monkeypatch.setattr("subprocess.call", fake_call)
    create_tag.create_tag()
    out = capsys.readouterr().out
    assert "Added tag for version 0.0.TEST" in out
    assert calls["cmd"] == ['git', 'tag', '--annotate', '0.0.TEST', '--message', 'Version 0.0.TEST']

def test_create_tag_failure(monkeypatch, capsys):
    def fake_call(cmd):
        return 1
    monkeypatch.setattr(create_tag, "read_version", lambda: "0.0.TEST", raising=False)
    monkeypatch.setattr("subprocess.call", fake_call)
    # Should not print anything on failure
    out_before = capsys.readouterr().out
    create_tag.create_tag()
    out_after = capsys.readouterr().out
    assert "Added tag" not in out_after
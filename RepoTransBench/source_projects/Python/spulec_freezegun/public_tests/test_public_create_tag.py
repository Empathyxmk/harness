import os
import sys
import tempfile
import types

import pytest

import importlib.util


def load_create_tag_module():
    # Load create_tag.py from the project root, regardless of sys.path
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'create_tag.py'))
    spec = importlib.util.spec_from_file_location("create_tag", path)
    create_tag = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(create_tag)
    return create_tag

def test_public_read_version(tmp_path, monkeypatch):
    create_tag = load_create_tag_module()
    version_code = "__version__ = '2.8.9a-public'\n"
    freezegun_dir = tmp_path / "freezegun"
    freezegun_dir.mkdir()
    (freezegun_dir / "__init__.py").write_text(version_code)
    orig_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = create_tag.read_version()
    finally:
        os.chdir(orig_cwd)
    assert result == '2.8.9a-public'

def test_public_create_tag(monkeypatch):
    create_tag = load_create_tag_module()
    called_args = {}

    def fake_read_version():
        return "0.0.21"

    def fake_call(cmd):
        called_args["cmd"] = cmd
        return 0

    monkeypatch.setattr(create_tag, "read_version", fake_read_version)
    import subprocess
    monkeypatch.setattr(subprocess, "call", fake_call)
    out_lines = []

    def fake_print(msg):
        out_lines.append(msg)
    monkeypatch.setattr("builtins.print", fake_print)
    create_tag.create_tag()
    assert called_args["cmd"][:5] == ['git', 'tag', '--annotate', '0.0.21', '--message']
    assert "0.0.21" in out_lines[0]
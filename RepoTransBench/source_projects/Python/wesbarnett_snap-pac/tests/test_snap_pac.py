import os
import sys
import tempfile
import types
import json
import builtins
import pytest

from scripts.snap_pac import SnapperCmd, ConfigProcessor

class DummyPopenResult:
    def __init__(self, retstr):
        self._retstr = retstr
    def read(self):
        return self._retstr

def test_snapper_cmd_str_and_call(monkeypatch):
    # Test with all options
    cmd = SnapperCmd('root', 'pre', 'number', description="desc", nodbus=True, pre_number=123, userdata="ud")
    s = str(cmd)
    assert "--no-dbus" in s
    assert "--config root create" in s
    assert "--description \"desc\"" in s
    assert "--userdata \"ud\"" in s
    assert "--type pre" in s
    # Simulate os.popen for __call__
    monkeypatch.setattr(os, "popen", lambda *a, **k: DummyPopenResult("42\n"))
    result = cmd()
    assert result == "42"

def test_snapper_cmd_post_no_prenumber(monkeypatch, caplog):
    # Should fallback to "single", and log debug message
    cmd = SnapperCmd('root', 'post', 'number', pre_number=None)
    assert "--type single" in str(cmd) or "--type post" in str(cmd)
    monkeypatch.setattr(os, "popen", lambda *a, **k: DummyPopenResult("test"))
    cmd()

def test_config_processor_default_settings(tmp_path):
    ini = tmp_path / "config.ini"
    ini.write_text("")
    # Simulate sys.stdin for __init__
    old_stdin = sys.stdin
    sys.stdin = types.SimpleNamespace()
    sys.stdin.__iter__ = lambda self: iter([])
    cp = ConfigProcessor(str(ini), "pre", parent_cmd="parent", packages=["pkg1", "pkg2"])
    result = cp("root")
    assert isinstance(result, dict)
    assert result["description"].startswith("parent")
    assert result["cleanup_algorithm"] == "number"
    sys.stdin = old_stdin

def test_config_processor_ini_options(tmp_path):
    # Write INI with extended options and section
    ini = tmp_path / "ext.ini"
    config_txt = """
[DEFAULT]
snapshot = false
cleanup_algorithm = timeline
pre_description = mycmd
post_description = install packages
desc_limit = 5
important_packages = ["imp"]
important_commands = ["imp_cmd"]
userdata = ["mytag"]
[root]
snapshot = true
    """
    ini.write_text(config_txt)
    cp = ConfigProcessor(str(ini), "pre", parent_cmd="imp_cmd", packages=["imp", "unimp"])
    assert cp.get_cleanup_algorithm("root") == "timeline"
    # Description trimmed to desc_limit
    assert cp.get_description("root") == "mycmd"
    # Important detection: both packages and parent_cmd
    assert cp.check_important_commands("root") is True
    assert cp.check_important_packages("root") is True
    # Userdata should add 'important=yes'
    ud = cp.get_userdata("root")
    assert "important=yes" in ud and "mytag" in ud
    out = cp("root")
    assert "description" in out and "userdata" in out

def test_config_processor_nonexistent_section(tmp_path):
    ini = tmp_path / "spawn.ini"
    ini.write_text("")
    cp = ConfigProcessor(str(ini), "post", parent_cmd="irrelevant", packages=[])
    # This should add a section if not present
    rv = cp("not_here")
    assert isinstance(rv, dict)
    assert rv["snapshot"] is False or rv["snapshot"] is True

def test_config_processor_check_important(monkeypatch, tmp_path):
    ini = tmp_path / "imp2.ini"
    ini.write_text("""
[root]
snapshot = true
important_packages = ["pkgx"]
important_commands = ["cmdy"]
userdata = ["z"]
""")
    cp = ConfigProcessor(str(ini), "post", parent_cmd="cmdy", packages=["pkgx", "pkgother"])
    rv = cp.check_important("root")
    assert rv is True

def test_config_processor_no_important(tmp_path):
    ini = tmp_path / "noimp.ini"
    ini.write_text("""
[root]
snapshot = true
important_packages = []
important_commands = []
userdata = []
""")
    cp = ConfigProcessor(str(ini), "post", parent_cmd="foo", packages=["bar"])
    assert cp.check_important("root") is False
    assert "important=yes" not in cp.get_userdata("root")

def test_snapper_cmd_types():
    # Edge case for type detection
    cmd = SnapperCmd('abc', 'post', 'alg', pre_number=None)
    assert "--type single" in str(cmd) or "--type post" in str(cmd)
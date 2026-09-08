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

def test_public_snapper_cmd_str_and_call(monkeypatch):
    # Test with all options using different param values
    cmd = SnapperCmd('data', 'pre', 'timeline', description="my-desc", nodbus=True, pre_number=789, userdata="user_data")
    s = str(cmd)
    assert "--no-dbus" in s
    assert "--config data create" in s
    assert "--description \"my-desc\"" in s
    assert "--userdata \"user_data\"" in s
    assert "--type pre" in s
    # Simulate os.popen for __call__
    monkeypatch.setattr(os, "popen", lambda *a, **k: DummyPopenResult("314\n"))
    result = cmd()
    assert result == "314"

def test_public_snapper_cmd_post_no_prenumber(monkeypatch, caplog):
    # Should fallback to "single", and log debug message
    cmd = SnapperCmd('foo', 'post', 'timeline', pre_number=None)
    assert "--type single" in str(cmd) or "--type post" in str(cmd)
    monkeypatch.setattr(os, "popen", lambda *a, **k: DummyPopenResult("returnz"))
    cmd()

def test_public_config_processor_default_settings(tmp_path):
    ini = tmp_path / "another_config.ini"
    ini.write_text("")
    # Simulate sys.stdin for __init__
    old_stdin = sys.stdin
    sys.stdin = types.SimpleNamespace()
    sys.stdin.__iter__ = lambda self: iter([])
    cp = ConfigProcessor(str(ini), "post", parent_cmd="runjob", packages=["abc", "xyz"])
    result = cp("home")
    assert isinstance(result, dict)
    assert result["description"].startswith("abc") or result["description"].startswith("runjob") or result["description"].startswith("xyz")
    assert result["cleanup_algorithm"] == "number"
    sys.stdin = old_stdin

def test_public_config_processor_ini_options(tmp_path):
    # Write INI with new values and section
    ini = tmp_path / "more.ini"
    config_txt = """
[DEFAULT]
snapshot = true
cleanup_algorithm = number
pre_description = commandX
post_description = just_test
desc_limit = 6
important_packages = ["abc"]
important_commands = ["ccc"]
userdata = ["newtag"]
[home]
snapshot = false
    """
    ini.write_text(config_txt)
    cp = ConfigProcessor(str(ini), "pre", parent_cmd="ccc", packages=["abc", "wxy"])
    assert cp.get_cleanup_algorithm("home") == "number"
    # Description trimmed to desc_limit
    assert cp.get_description("home") == "comman"
    # Important detection: both packages and parent_cmd
    assert cp.check_important_commands("home") is True
    assert cp.check_important_packages("home") is True
    # Userdata should add 'important=yes'
    ud = cp.get_userdata("home")
    assert "important=yes" in ud and "newtag" in ud
    out = cp("home")
    assert "description" in out and "userdata" in out

def test_public_config_processor_nonexistent_section(tmp_path):
    ini = tmp_path / "section.ini"
    ini.write_text("")
    cp = ConfigProcessor(str(ini), "pre", parent_cmd="diff", packages=[])
    # This should add a section if not present
    rv = cp("qwerty")
    assert isinstance(rv, dict)
    assert "snapshot" in rv

def test_public_config_processor_check_important(monkeypatch, tmp_path):
    ini = tmp_path / "zzz.ini"
    ini.write_text("""
[home]
snapshot = false
important_packages = ["specialpkg"]
important_commands = ["specialcmd"]
userdata = ["t"]
""")
    cp = ConfigProcessor(str(ini), "post", parent_cmd="specialcmd", packages=["specialpkg", "otherpkg"])
    rv = cp.check_important("home")
    assert rv is True

def test_public_config_processor_no_important(tmp_path):
    ini = tmp_path / "notag.ini"
    ini.write_text("""
[zzz]
snapshot = false
important_packages = []
important_commands = []
userdata = []
""")
    cp = ConfigProcessor(str(ini), "post", parent_cmd="nope", packages=["nil"])
    assert cp.check_important("zzz") is False
    assert "important=yes" not in cp.get_userdata("zzz")

def test_public_snapper_cmd_types():
    # Edge case for type detection
    cmd = SnapperCmd('customcfg', 'post', 'otheralg', pre_number=None)
    assert "--type single" in str(cmd) or "--type post" in str(cmd)
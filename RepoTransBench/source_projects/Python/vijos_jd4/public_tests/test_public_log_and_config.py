import os
import sys
import types
import builtins
import pytest
import importlib
from unittest import mock

@pytest.fixture(autouse=True)
def cleanup_log_import(monkeypatch):
    """Cleanup after log import so coloredlogs doesn't persist settings."""
    modules_before = set(sys.modules)
    yield
    for mod in list(sys.modules):
        if mod.startswith("coloredlogs"):
            sys.modules.pop(mod, None)
    sys.modules.pop("jd4.log", None)

def test_public_log_install(monkeypatch):
    # Simulate absence of JD4_USE_SYSLOG -> coloredlogs.install called
    monkeypatch.delenv('JD4_USE_SYSLOG', raising=False)
    installed = {}
    class FakeColoredLogs:
        def install(self, **kwargs):
            installed['invoked'] = kwargs
    sys.modules['coloredlogs'] = FakeColoredLogs()
    sys.modules['coloredlogs.syslog'] = types.SimpleNamespace(enable_system_logging=None)
    sys.modules.pop('jd4.log', None)
    import jd4.log
    assert 'invoked' in installed

def test_public_log_syslog(monkeypatch):
    os.environ['JD4_USE_SYSLOG'] = "yes"
    called = {}
    sysmodules_backup = dict(sys.modules)
    class FakeSyslog:
        def enable_system_logging(self, **kwargs):
            called['syslog2'] = kwargs
    sys.modules['coloredlogs'] = types.SimpleNamespace(install=None)
    sys.modules['coloredlogs.syslog'] = FakeSyslog()
    sys.modules.pop('jd4.log', None)
    import jd4.log
    assert 'syslog2' in called
    del os.environ['JD4_USE_SYSLOG']
    sys.modules = sysmodules_backup

def test_public_config_file_not_found(tmp_path, monkeypatch):
    from jd4 import config as config_module
    import importlib
    import sys
    sys.modules.pop("jd4.config", None)
    sys.modules.pop("jd4.log", None)
    monkeypatch.setattr("appdirs.user_config_dir", lambda x: str(tmp_path))
    # Patch logger, patch exit to throw SystemExit
    error_calls = []
    fake_logger = types.SimpleNamespace(error=lambda *args, **kwargs: error_calls.append((args, kwargs)))
    monkeypatch.setattr("jd4.log.logger", fake_logger)
    monkeypatch.setattr("builtins.exit", lambda code=12: (_ for _ in ()).throw(SystemExit(code)))
    # Patch yaml to use a dummy YAML parser
    class DummyYaml:
        def load(self, f):
            return {'b': 15}
    monkeypatch.setattr("ruamel.yaml.YAML", lambda: DummyYaml())
    config_path = tmp_path / "config.yaml"
    assert not config_path.exists()
    with pytest.raises(SystemExit):
        importlib.reload(__import__("jd4.config"))
    assert error_calls
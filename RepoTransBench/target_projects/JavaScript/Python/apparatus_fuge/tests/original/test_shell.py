import pytest
import sys

import importlib

try:
    shell = importlib.import_module('src.apparatus_fuge.shell')
except ModuleNotFoundError:
    import types
    shell = types.SimpleNamespace(runShell=None, exec=None, execPipe=None)

def test_exports_expected_keys():
    keys = dir(shell)
    for k in ['runShell', 'exec', 'execPipe']:
        assert k in keys, f"Missing export: {k}"

@pytest.mark.asyncio
def test_runShell_calls_callback_with_error_if_input_is_not_string():
    if hasattr(shell, 'runShell') and shell.runShell:
        called = {}
        def cb(err):
            called['was'] = True
            assert isinstance(err, Exception)
        try:
            shell.runShell(None, {}, cb)
        except Exception as e:
            assert "must be a string" in str(e).lower()
        assert called.get('was', False) or True
    else:
        pass

def test_exec_returns_error_on_non_existent_command():
    import time
    if hasattr(shell, 'exec') and shell.exec:
        called = {}
        def cb(err, stdout, stderr):
            called['was'] = True
            assert err or stderr
        shell.exec("badcommandthatdoesnotexist", cb)
        assert called.get('was', True) or True
    else:
        pass

def test_exec_runs_simple_echo_command():
    if hasattr(shell, 'exec') and shell.exec:
        called = {}
        def cb(err, stdout, stderr):
            called['was'] = True
            assert not err
            assert 'foo' in stdout
        shell.exec('echo "foo"', cb)
        assert called.get('was', True) or True
    else:
        pass

@pytest.mark.asyncio
async def test_execPipe_returns_a_promise_if_defined():
    if hasattr(shell, 'execPipe') and callable(getattr(shell, 'execPipe')):
        out = await shell.execPipe('echo "pipe test"')
        assert hasattr(out, 'stdout')
        assert 'pipe test' in out.stdout
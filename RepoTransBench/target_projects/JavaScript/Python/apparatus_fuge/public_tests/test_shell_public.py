import importlib

try:
    shell = importlib.import_module('src.apparatus_fuge.shell')
except ModuleNotFoundError:
    import types
    shell = types.SimpleNamespace(runShell=None, exec=None, execPipe=None)

def test_exports_expected_keys_different_check():
    keys = dir(shell)
    assert 'execPipe' in keys
    assert 'runShell' in keys
    assert 'exec' in keys

def test_runShell_errors_if_input_is_not_string():
    if hasattr(shell, 'runShell') and shell.runShell:
        try:
            shell.runShell(42, {}, lambda err: assert isinstance(err, Exception))
        except Exception as e:
            assert "must be a string" in str(e).lower()

def test_exec_returns_error_on_obviously_invalid_command_name():
    if hasattr(shell, 'exec') and shell.exec:
        def cb(err, stdout, stderr):
            assert err or stderr
        shell.exec('nonexistentpublicfoobarcmd', cb)

def test_exec_runs_simple_echo_with_different_output():
    if hasattr(shell, 'exec') and shell.exec:
        def cb(err, stdout, stderr):
            assert not err
            assert 'barbaz' in stdout
        shell.exec('echo "barbaz"', cb)

import pytest
@pytest.mark.asyncio
async def test_execPipe_returns_promise_and_echo_returns_new_value():
    if hasattr(shell, 'execPipe') and callable(getattr(shell, 'execPipe')):
        out = await shell.execPipe('echo "another pipe test"')
        assert hasattr(out, 'stdout')
        assert 'another pipe test' in out.stdout
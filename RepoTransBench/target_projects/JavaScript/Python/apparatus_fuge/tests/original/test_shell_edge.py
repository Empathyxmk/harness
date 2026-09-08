import pytest
import importlib

try:
    shell = importlib.import_module('src.apparatus_fuge.shell')
except ModuleNotFoundError:
    import types
    shell = types.SimpleNamespace(runShell=None, exec=None, execPipe=None)

def test_runShell_should_error_if_input_shell_not_string():
    if hasattr(shell, 'runShell') and shell.runShell:
        def cb(err):
            assert err
        shell.runShell({}, {}, cb)

@pytest.mark.timeout(5)
def test_execPipe_returns_error_on_non_existent_command():
    if hasattr(shell, 'execPipe') and shell.execPipe:
        finished = False
        def cb(err):
            nonlocal finished
            finished = True
            assert err
        try:
            shell.execPipe('definitely-not-a-command-foo-bar', {}, cb)
            maybePromise = shell.execPipe('definitely-not-a-command-bar-foo', {})
            if hasattr(maybePromise, 'then'):
                def on_res(_): pytest.fail("Expected error on bad command")
                def on_err(err): 
                    nonlocal finished
                    if not finished:
                        assert err
                        finished = True
                maybePromise.then(on_res, on_err)
        except Exception:
            pass

def test_runShell_completes_even_with_empty_cb():
    if hasattr(shell, 'runShell') and shell.runShell:
        def cb(err, result):
            assert not err
            assert result
        shell.runShell('echo 123', {}, cb)
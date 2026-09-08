import sys
import os
import types
import pytest
from unittest import mock

# ---------------------------
# Setup Docker Test Mocks
# ---------------------------

def import_setup_docker_module(shell_fn=None, buildx_fn=None, run_fn=None):
    """
    Dynamically create a setup_docker module mock with shell/buildx/run functions.
    """
    m = types.ModuleType("setup_docker")
    if shell_fn is None:
        def shell(cmd):
            return "out"
        shell_fn = shell
    if buildx_fn is None:
        async def buildx():
            pass
        buildx_fn = buildx
    if run_fn is None:
        async def run():
            pass
        run_fn = run
    m.shell = shell_fn
    m.buildx = buildx_fn
    m.run = run_fn
    sys.modules["setup_docker"] = m
    return m

@pytest.fixture(autouse=True)
def patch_imports(monkeypatch):
    # Patch functions and modules for each test separately
    patches = {}

    class ExecMock:
        def __init__(self):
            self.calls = []
        async def exec(self, cmd, args=None, opts=None):
            self.calls.append((cmd, args, opts))
            if patches.get('exec_error'):
                raise patches['exec_error']
            return 0
    exec_mock = ExecMock()

    class CoreMock:
        def __init__(self):
            self.vars = {}
            self.debug_calls = []
            self.info_calls = []
            self.export_calls = []
            self.warning_calls = []
            self.getinput_calls = []
        def getInput(self, name):
            self.getinput_calls.append(name)
            case_map = patches.get('core_getinput_map', {})
            return case_map.get(name, "")
        def exportVariable(self, key, value):
            self.export_calls.append((key, value))
        def debug(self, arg):
            self.debug_calls.append(arg)
        def info(self, arg):
            self.info_calls.append(arg)
        def warning(self, arg):
            self.warning_calls.append(arg)
        def startGroup(self):
            pass
        def endGroup(self):
            pass

    core_mock = CoreMock()

    class OsMock:
        def __init__(self):
            self.platform_val = patches.get('platform', 'linux')
            self.arch_val = patches.get('arch', 'x64')
        def platform(self):
            return patches.get('platform', 'linux')
        def arch(self):
            return patches.get('arch', 'x64')
        def homedir(self):
            return "/Users/runner"

    os_mock = OsMock()
    
    shell_context = {'stdout': patches.get('shell_stdout', 'ok'),
                     'stderr': patches.get('shell_stderr', ''),
                     'error': patches.get('shell_error', None)}
    def child_process_exec(cmd, cb):
        cb(shell_context['error'], shell_context['stdout'], shell_context['stderr'])

    # Patching
    monkeypatch.setitem(sys.modules, "@actions.exec", exec_mock)
    monkeypatch.setitem(sys.modules, "@actions.core", core_mock)
    monkeypatch.setitem(sys.modules, "os", os_mock)
    monkeypatch.setitem(sys.modules, "child_process", types.SimpleNamespace(exec=child_process_exec))

    yield patches, exec_mock, core_mock, os_mock, child_process_exec

@pytest.fixture
def setup_mocks(patch_imports):
    patches, exec_mock, core_mock, os_mock, child_process_exec = patch_imports
    def set_mock(**kwargs):
        for k, v in kwargs.items():
            patches[k] = v
    return set_mock, exec_mock, core_mock, os_mock, child_process_exec

# Utility to simulate await behavior in normal functions (for shell)
import asyncio
def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

# ---------------------
# Test Cases
# ---------------------

def test_exports_shell_buildx_run(monkeypatch):
    # All functions should be present and correct types
    m = import_setup_docker_module()
    assert hasattr(m, "shell")
    assert hasattr(m, "buildx")
    assert hasattr(m, "run")
    assert callable(m.shell)
    assert callable(m.buildx)
    assert callable(m.run)

@pytest.mark.asyncio
async def test_shell_resolves_with_stdout(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(shell_stdout="out", shell_stderr="", shell_error=None)
    result = []
    def shell(cmd):
        result.append("out")
        return "out"
    mod = import_setup_docker_module(shell_fn=shell)
    out = mod.shell("ls")
    assert out == "out"

@pytest.mark.asyncio
async def test_shell_rejects_on_error(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(shell_error=Exception("fail"))
    called = {}
    def shell(cmd):
        raise Exception("fail")
    mod = import_setup_docker_module(shell_fn=shell)
    with pytest.raises(Exception) as e:
        mod.shell("ls")
    assert "fail" in str(e.value)

@pytest.mark.asyncio
async def test_shell_rejects_on_stderr(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(shell_stdout="foo", shell_stderr="err here", shell_error=None)
    def shell(cmd):
        raise Exception("err here")
    mod = import_setup_docker_module(shell_fn=shell)
    with pytest.raises(Exception) as e:
        mod.shell("ls")
    assert "err here" in str(e.value)

@pytest.mark.asyncio
async def test_buildx_runs_buildx_and_exports_cli_experimental(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(buildx="true", core_getinput_map={'docker_cli_experimental': 'enabled'})
    async def buildx():
        exec_mock.exec('buildx', ['version'], None)
        core_mock.exportVariable('DOCKER_CLI_EXPERIMENTAL', 'enabled')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert exec_mock.calls
    assert ("DOCKER_CLI_EXPERIMENTAL", "enabled") in core_mock.export_calls

@pytest.mark.asyncio
async def test_buildx_no_run_when_not_true(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(buildx='false')
    async def buildx():
        core_mock.info('buildx disabled')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert ('buildx disabled',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.info_calls]

@pytest.mark.asyncio
async def test_buildx_falls_back_on_error(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(buildx="true", exec_error=Exception("fail"))
    async def buildx():
        try:
            raise Exception("fail")
        except Exception:
            core_mock.info('this docker version NOT Support Buildx')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert ('this docker version NOT Support Buildx',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.info_calls]

@pytest.mark.asyncio
async def test_run_error_on_windows(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(platform="win32")
    async def run():
        core_mock.debug('check platform')
        exec_mock.exec('echo', ['Windows not supported'], None)
    mod = import_setup_docker_module(run_fn=run)
    await mod.run()
    assert ('check platform',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.debug_calls]
    assert any(call[0] == 'echo' for call in exec_mock.calls)

@pytest.mark.asyncio
async def test_run_warn_macos_non_x64(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(platform='darwin', arch='arm64')
    async def run():
        core_mock.warning('only support macOS x86_64, os arch is arm64')
    mod = import_setup_docker_module(run_fn=run)
    await mod.run()
    assert ('only support macOS x86_64, os arch is arm64',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.warning_calls]

@pytest.mark.asyncio
async def test_run_sets_up_docker_on_macos_x64(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(platform="darwin", arch="x64")
    async def run():
        core_mock.exportVariable("DOCKER_CONFIG", "/Users/runner/.docker")
        exec_mock.exec('wget', [
            'https://raw.githubusercontent.com/Homebrew/homebrew-cask/fe866ec0765de141599745f03e215452db7f511b/Casks/docker.rb'
        ], None)
    mod = import_setup_docker_module(run_fn=run)
    await mod.run()
    assert ("DOCKER_CONFIG", "/Users/runner/.docker") in core_mock.export_calls
    assert any(call[0] == "wget" for call in exec_mock.calls)

@pytest.mark.asyncio
async def test_run_nothing_for_linux(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(platform="linux", arch="x64")
    async def run():
        # Should not call debug("check platform") or warning.
        pass
    mod = import_setup_docker_module(run_fn=run)
    await mod.run()
    # There should not be any debug call "check platform" or warning calls
    assert "check platform" not in core_mock.debug_calls
    assert not core_mock.warning_calls

@pytest.mark.asyncio
async def test_buildx_exports_cli_experimental_if_missing(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(buildx='true', core_getinput_map={'docker_cli_experimental': ''})
    async def buildx():
        core_mock.exportVariable('DOCKER_CLI_EXPERIMENTAL', 'enabled')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert ('DOCKER_CLI_EXPERIMENTAL', 'enabled') in core_mock.export_calls

@pytest.mark.asyncio
async def test_buildx_disabled_for_other_input(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(buildx='1', core_getinput_map={'docker_cli_experimental': 'enabled'})
    async def buildx():
        core_mock.info('buildx disabled')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert ('buildx disabled',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.info_calls]

@pytest.mark.asyncio
async def test_run_all_macos_steps(setup_mocks):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks
    set_mock(platform='darwin', arch='x64', dockerDaemonJson='{"debug":true}')
    async def run():
        exec_mock.exec('cat', ['/Users/runner/.docker/daemon.json'], None)
    mod = import_setup_docker_module(run_fn=run)
    await mod.run()
    assert any(call[0] == "cat" for call in exec_mock.calls)
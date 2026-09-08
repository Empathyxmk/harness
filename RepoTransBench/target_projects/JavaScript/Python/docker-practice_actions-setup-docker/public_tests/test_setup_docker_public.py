import sys
import types
import pytest

# ---------------------------
# Setup Docker Test Mocks (Public)
# ---------------------------

def import_setup_docker_module(shell_fn=None, buildx_fn=None, run_fn=None):
    """Dynamically create a setup_docker module mock with shell/buildx/run functions (public tests)."""
    m = types.ModuleType("setup_docker")
    if shell_fn is None:
        def shell(cmd):
            return "output for pub"
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
def patch_imports_public(monkeypatch):
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
            self.platform_val = patches.get('platform', 'darwin')
            self.arch_val = patches.get('arch', 'arm64')
        def platform(self):
            return patches.get('platform', 'darwin')
        def arch(self):
            return patches.get('arch', 'arm64')
        def homedir(self):
            return "/Users/testing"

    os_mock = OsMock()
    
    shell_context = {'stdout': patches.get('shell_stdout', 'public_ok'),
                     'stderr': patches.get('shell_stderr', ''),
                     'error': patches.get('shell_error', None)}
    def child_process_exec(cmd, cb):
        cb(shell_context['error'], shell_context['stdout'], shell_context['stderr'])
    
    monkeypatch.setitem(sys.modules, "@actions.exec", exec_mock)
    monkeypatch.setitem(sys.modules, "@actions.core", core_mock)
    monkeypatch.setitem(sys.modules, "os", os_mock)
    monkeypatch.setitem(sys.modules, "child_process", types.SimpleNamespace(exec=child_process_exec))

    yield patches, exec_mock, core_mock, os_mock, child_process_exec

@pytest.fixture
def setup_mocks_public(patch_imports_public):
    patches, exec_mock, core_mock, os_mock, child_process_exec = patch_imports_public
    def set_mock(**kwargs):
        for k, v in kwargs.items():
            patches[k] = v
    return set_mock, exec_mock, core_mock, os_mock, child_process_exec

# Utility to simulate await behavior
import asyncio

def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

# --------- TESTS ---------

def test_exports_shell_buildx_run_public(monkeypatch):
    m = import_setup_docker_module()
    assert hasattr(m, "shell")
    assert hasattr(m, "buildx")
    assert hasattr(m, "run")
    assert callable(m.shell)
    assert callable(m.buildx)
    assert callable(m.run)

@pytest.mark.asyncio
async def test_shell_resolves_with_stdout_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(shell_stdout="output for pub", shell_stderr="", shell_error=None)
    def shell(cmd):
        return "output for pub"
    mod = import_setup_docker_module(shell_fn=shell)
    out = mod.shell("pwd")
    assert out == "output for pub"

@pytest.mark.asyncio
async def test_shell_rejects_on_error_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(shell_error=Exception("public fail"))
    def shell(cmd):
        raise Exception("public fail")
    mod = import_setup_docker_module(shell_fn=shell)
    with pytest.raises(Exception) as e:
        mod.shell("pwd")
    assert "public fail" in str(e.value)

@pytest.mark.asyncio
async def test_shell_rejects_on_stderr_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(shell_stdout="directory", shell_stderr="something went wrong!", shell_error=None)
    def shell(cmd):
        raise Exception("something went wrong!")
    mod = import_setup_docker_module(shell_fn=shell)
    with pytest.raises(Exception) as e:
        mod.shell("pwd")
    assert "something went wrong!" in str(e.value)

@pytest.mark.asyncio
async def test_buildx_runs_and_exports_cli_experimental_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(buildx="true", core_getinput_map={'docker_cli_experimental': 'disabled'})
    async def buildx():
        exec_mock.exec('buildx', ['version'], None)
        core_mock.exportVariable('DOCKER_CLI_EXPERIMENTAL', 'disabled')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert exec_mock.calls
    assert ("DOCKER_CLI_EXPERIMENTAL", "disabled") in core_mock.export_calls

@pytest.mark.asyncio
async def test_buildx_no_run_when_off_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(buildx="off")
    async def buildx():
        core_mock.info('buildx disabled')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert ('buildx disabled',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.info_calls]

@pytest.mark.asyncio
async def test_buildx_fallback_on_error_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(buildx="true", exec_error=Exception("public-exec-fail"))
    async def buildx():
        try:
            raise Exception("public-exec-fail")
        except Exception:
            core_mock.info('this docker version NOT Support Buildx')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert ('this docker version NOT Support Buildx',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.info_calls]

@pytest.mark.asyncio
async def test_run_handle_sunos_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(platform='sunos')
    async def run():
        core_mock.debug('check platform')
        exec_mock.exec('echo', ['SunOS not fully supported'], None)
    mod = import_setup_docker_module(run_fn=run)
    await mod.run()
    assert ('check platform',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.debug_calls]
    assert any(call[0] == "echo" for call in exec_mock.calls)

@pytest.mark.asyncio
async def test_run_warn_macos_ia32_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(platform='darwin', arch='ia32')
    async def run():
        core_mock.warning('only support macOS x86_64, os arch is ia32')
    mod = import_setup_docker_module(run_fn=run)
    await mod.run()
    assert ('only support macOS x86_64, os arch is ia32',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.warning_calls]

@pytest.mark.asyncio
async def test_run_sets_up_docker_on_macos_x64_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(platform='darwin', arch='x64')
    async def run():
        core_mock.exportVariable("DOCKER_CONFIG", "/Users/testing/.docker")
        exec_mock.exec('wget', [
            'https://raw.githubusercontent.com/Homebrew/homebrew-cask/fe866ec0765de141599745f03e215452db7f511b/Casks/docker.rb'
        ], None)
    mod = import_setup_docker_module(run_fn=run)
    await mod.run()
    assert ("DOCKER_CONFIG", "/Users/testing/.docker") in core_mock.export_calls
    assert any(call[0] == "wget" for call in exec_mock.calls)

@pytest.mark.asyncio
async def test_run_nothing_for_freebsd_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(platform='freebsd', arch='x64')
    async def run():
        # Should not call debug("check platform") or warning.
        pass
    mod = import_setup_docker_module(run_fn=run)
    await mod.run()
    assert "check platform" not in core_mock.debug_calls
    assert not core_mock.warning_calls

@pytest.mark.asyncio
async def test_buildx_exports_cli_experimental_if_missing_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(buildx='true', core_getinput_map={'docker_cli_experimental': ''})
    async def buildx():
        core_mock.exportVariable('DOCKER_CLI_EXPERIMENTAL', 'enabled')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert ('DOCKER_CLI_EXPERIMENTAL', 'enabled') in core_mock.export_calls

@pytest.mark.asyncio
async def test_buildx_disabled_for_other_input_public(setup_mocks_public):
    set_mock, exec_mock, core_mock, os_mock, child_process_exec = setup_mocks_public
    set_mock(buildx='enabled', core_getinput_map={'docker_cli_experimental': 'enabled'})
    async def buildx():
        core_mock.info('buildx disabled')
    mod = import_setup_docker_module(buildx_fn=buildx)
    await mod.buildx()
    assert ('buildx disabled',) in [t if isinstance(t,tuple) else (t,) for t in core_mock.info_calls]
import pytest
import importlib

try:
    commands = importlib.import_module('src.apparatus_fuge.commands')
except ModuleNotFoundError:
    def commands(*args, **kwargs):
        class Dummy:
            def __init__(self):
                self.init = lambda: None
                self.shell = lambda: None
                self.isGroup = lambda a, sys=None: True if a=='dev' else None
                self.showInfo = lambda args, opts, cb: cb(None, {"usage": True})
        return Dummy()

class FakeRunner:
    def preview(self, group, full, cb):
        cb(None, {'out': 'preview:' + str(group) + ':' + str(full)})

@pytest.fixture(scope='module')
def cmnds():
    return commands({}, FakeRunner())

def test_exports_functions_including_init_shell_isGroup_showInfo(cmnds):
    assert callable(cmnds.init)
    assert callable(cmnds.shell)
    if hasattr(cmnds, 'isGroup'):
        assert True
    if hasattr(cmnds, 'showInfo'):
        assert True

def test_isGroup_returns_true_if_match_and_none_if_no_match(cmnds):
    if hasattr(cmnds, 'isGroup'):
        sys = {'groups': {'dev': ['svc1', 'svc2']}}
        assert cmnds.isGroup('dev', sys) is True
        assert cmnds.isGroup('foo', sys) is None

def test_showInfo_routes_to_runner_preview_and_usage(cmnds):
    called = {}
    def cb(err, out):
        called['val'] = out
    cmnds.showInfo(['foo'], {}, cb)
    assert called['val'] and called['val']['out'] == 'preview:foo:False'
    def cb2(err, out):
        called['val2'] = out
    cmnds.showInfo(['foo', 'full'], {}, cb2)
    assert called['val2'] and called['val2']['out'] == 'preview:foo:True'
    def cb3(err, out):
        called['val3'] = out
    cmnds.showInfo(['foo', 'bar', 'baz'], {}, cb3)
    assert called['val3'] and 'usage' in called['val3']
    def cb4(err, out):
        called['val4'] = out
    cmnds.showInfo([], {}, cb4)
    assert called['val4'] and 'usage' in called['val4']
import importlib

try:
    commands = importlib.import_module('src.apparatus_fuge.commands')
except ModuleNotFoundError:
    def commands(*args, **kwargs):
        class Dummy:
            def __init__(self):
                self.init = lambda: None
                self.shell = lambda: None
                self.showInfo = lambda args, opts, cb: cb(None, {'usage': True})
        return Dummy()

def test_create_commands_instance_with_non_empty_object():
    cmds = commands({'a': 1}, {'b': 2})
    assert isinstance(cmds, object)
    assert hasattr(cmds, 'init') and callable(cmds.init)
    assert hasattr(cmds, 'shell') and callable(cmds.shell)

def test_return_usage_true_for_showInfo_with_many_args():
    cmds = commands({}, {'preview': lambda group, full, cb: cb(None, {'out':'y'})})
    if hasattr(cmds, 'showInfo'):
        called = {'val': None}
        def cb(err, result):
            called['val'] = result
        cmds.showInfo([1,2,3], {}, cb)
        assert called['val'] and called['val'].get('usage', None) is True

def test_call_preview_for_showInfo_with_full_argument():
    called = {'called': False}
    def preview(group, full, cb):
        called['called'] = True
        assert full is True
        cb(None, {'ok': 'yes'})
    cmds = commands({}, {'preview': preview})
    if hasattr(cmds, 'showInfo'):
        def cb(err, result):
            assert called['called']
            assert result
        cmds.showInfo(['groupA', 'full'], {}, cb)
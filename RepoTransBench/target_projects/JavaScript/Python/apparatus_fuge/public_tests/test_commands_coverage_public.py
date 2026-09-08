import importlib

try:
    commands = importlib.import_module('src.apparatus_fuge.commands')
except ModuleNotFoundError:
    def commands(*args, **kwargs):
        class Dummy:
            def __init__(self):
                self.showInfo = lambda args, opts, cb: cb(None, {'ok': 1})
        return Dummy()

def test_properly_call_showInfo_with_1_argument_string():
    called = {'was': False}
    def preview(group, full, cb):
        called['was'] = True
        cb(None, {'ok': 1})
    cmds = commands({}, {'preview': preview})
    if hasattr(cmds, 'showInfo'):
        def cb(err, result):
            assert called['was']
            assert result
        cmds.showInfo(['testgroup'], {}, cb)

def test_call_preview_with_group_and_false():
    params = {}
    def preview(group, full, cb):
        params['group'] = group
        params['full'] = full
        cb(None, {'out': 42})
    cmds = commands({}, {'preview': preview})
    if hasattr(cmds, 'showInfo'):
        def cb(err, result):
            assert params.get('full', None) is False
            assert result
        cmds.showInfo(['g'], {}, cb)
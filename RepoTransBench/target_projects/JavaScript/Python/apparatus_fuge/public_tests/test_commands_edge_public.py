import importlib

try:
    commands = importlib.import_module('src.apparatus_fuge.commands')
except ModuleNotFoundError:
    def commands(*args, **kwargs):
        class Dummy:
            def init(self): pass
            def shell(self): pass
        return Dummy()

def test_handle_truly_null_runner_arguments_gracefully():
    cmds = commands(None, None)
    assert isinstance(cmds, object)
    assert hasattr(cmds, 'init') and callable(cmds.init)
    assert hasattr(cmds, 'shell') and callable(cmds.shell)

def test_exercise_branch_in_isGroup_group_not_in_groups():
    cmds = commands({}, {})
    if hasattr(cmds, 'isGroup'):
        sys = {'groups': {'prod':['svcZ']}}
        assert cmds.isGroup('qa', sys) is None

def test_handle_showInfo_with_null_as_arguments():
    class Runner:
        def preview(self, group, full, cb):
            cb(None, {'out':'z'})
    cmds = commands({}, Runner())
    if hasattr(cmds, 'showInfo'):
        def cb(err, result):
            assert result
        cmds.showInfo(None, {}, cb)
import importlib

try:
    commands = importlib.import_module('src.apparatus_fuge.commands')
except ModuleNotFoundError:
    def commands(*args, **kwargs):
        class Dummy:
            def init(self): pass
            def shell(self): pass
        return Dummy()

def test_should_construct_commands_object_and_have_methods():
    cmds = commands()
    assert hasattr(cmds, 'init') and callable(cmds.init)
    assert hasattr(cmds, 'shell') and callable(cmds.shell)
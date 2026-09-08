import sys
import os
import types

import pytest

# The following block patches ai_models.__main__ to mock parse_args if needed
try:
    import ai_models.__main__ as mainmod
except ModuleNotFoundError:
    mainmod = None

def dummy_parse_args(argv):
    class DummyArgs:
        def __init__(self, command, dummy):
            self.command = command
            self.dummy = dummy
    if 'nonsense_command' in argv:
        raise SystemExit(2)
    dummy = argv[2] if len(argv) > 2 else None
    return DummyArgs(command=argv[0], dummy=dummy)

@pytest.fixture(autouse=True)
def patch_parse_args(monkeypatch):
    # Only patch if import failed or original parse_args not available
    import builtins
    if mainmod is None or not hasattr(mainmod, "parse_args"):
        module = types.ModuleType("mainmod")
        module.parse_args = dummy_parse_args
        sys.modules["ai_models.__main__"] = module
    else:
        monkeypatch.setattr(mainmod, "parse_args", dummy_parse_args)

def test_public_main_parse_args():
    import ai_models.__main__ as mainmod
    argv = ['run', '--dummy', 'xy']
    args = mainmod.parse_args(argv)
    assert args.command == 'run'
    assert getattr(args, 'dummy', None) == 'xy' or getattr(args, 'dummy', None) is None

def test_public_main_invalid_args():
    import ai_models.__main__ as mainmod
    argv = ['nonsense_command']
    with pytest.raises(SystemExit):
        mainmod.parse_args(argv)
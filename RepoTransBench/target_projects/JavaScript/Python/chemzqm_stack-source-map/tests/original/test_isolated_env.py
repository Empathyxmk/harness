import pytest
import builtins
from src.stack_source_map import stack_source_map

class DummyConsole:
    def __init__(self):
        self.warnings = []

    def warn(self, message):
        self.warnings.append(message)

@pytest.fixture(autouse=True)
def patch_location_and_console(monkeypatch):
    # Save & set location/protocol and patch console
    orig_location = getattr(builtins, "location", None)
    orig_console = getattr(builtins, "console", None)
    builtins.location = type("Loc", (), {})()
    builtins.location.protocol = "file:"
    # Patch console to capture warnings
    console = DummyConsole()
    builtins.console = console
    yield console
    # Restore
    if orig_location is not None:
        builtins.location = orig_location
    else:
        del builtins.location
    if orig_console is not None:
        builtins.console = orig_console
    else:
        del builtins.console

def test_should_not_throw_and_warn_when_protocol_is_file(patch_location_and_console):
    # Confirm no exception, and warning about file protocol appears
    stack_source_map()
    matched = any("not works on file protocol" in msg for msg in patch_location_and_console.warnings)
    assert matched
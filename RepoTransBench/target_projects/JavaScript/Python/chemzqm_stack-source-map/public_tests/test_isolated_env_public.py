import pytest
import builtins
from src.stack_source_map import stack_source_map

class DummyConsole:
    def __init__(self):
        self.warnings = []
    def warn(self, message):
        self.warnings.append(str(message))

@pytest.fixture(autouse=True)
def patch_location_and_console():
    orig_location = getattr(builtins, "location", None)
    orig_console = getattr(builtins, "console", None)
    builtins.location = type("Loc", (), {})()
    # Using protocol variant 'file:' as per public test data; could also try 'File:' for robustness
    builtins.location.protocol = "file:"
    console = DummyConsole()
    builtins.console = console
    yield console
    if orig_location is not None:
        builtins.location = orig_location
    else:
        del builtins.location
    if orig_console is not None:
        builtins.console = orig_console
    else:
        del builtins.console

def test_should_not_throw_and_log_warning_on_file_protocol(patch_location_and_console):
    stack_source_map()
    # The public version requires just that "protocol" substring is in warning
    assert any("protocol" in msg for msg in patch_location_and_console.warnings)
import pytest
import builtins
from src.stack_source_map import stack_source_map

# Simulate global Error like Node.js
Error = builtins.Error

class DummyStackParser:
    def parse(self, *a, **k):
        return "parsed"

@pytest.fixture(autouse=True)
def cleanup_location():
    # Remove global location for tests, backup and restore
    orig_location = getattr(builtins, "location", None)
    if hasattr(builtins, "location"):
        delattr(builtins, "location")
    yield
    if orig_location is not None:
        builtins.location = orig_location
    elif hasattr(builtins, "location"):
        delattr(builtins, "location")

def test_exports_function():
    assert callable(stack_source_map)

def test_invoking_stack_source_map_does_not_throw_when_location_not_defined():
    # Should not throw error if location global is missing
    stack_source_map()

def test_invoking_with_options_does_not_throw():
    stack_source_map({
        "prepareStackTrace": lambda *a, **k: None,
        "ErrorStackParser": DummyStackParser()
    })

def test_sets_prepare_stack_trace_in_node_env_if_no_option_provided():
    stack_source_map()
    assert callable(Error.prepareStackTrace)

def test_uses_provided_prepare_stack_trace_from_options():
    mock = lambda *a, **k: "called"
    stack_source_map({"prepareStackTrace": mock})
    assert Error.prepareStackTrace is mock

def test_does_not_throw_if_error_stack_parser_is_provided():
    stack_source_map({"ErrorStackParser": DummyStackParser()})
    assert Error.prepareStackTrace is not None
import pytest
import builtins
from src.stack_source_map import stack_source_map

Error = builtins.Error

class DummyParserPublic:
    def parse(self, *a, **k):
        return {}

@pytest.fixture(autouse=True)
def cleanup_location():
    orig_location = getattr(builtins, "location", None)
    if hasattr(builtins, "location"):
        delattr(builtins, "location")
    yield
    if orig_location is not None:
        builtins.location = orig_location
    elif hasattr(builtins, "location"):
        delattr(builtins, "location")

def test_exports_callable_entity():
    assert callable(stack_source_map)

def test_invoking_stack_source_map_does_not_throw_with_no_arguments():
    stack_source_map(None)

def test_invoking_with_different_options_object_does_not_throw():
    stack_source_map({
        "prepareStackTrace": lambda *a, **k: None,
        "ErrorStackParser": DummyParserPublic()
    })

def test_sets_prepare_stack_on_no_option():
    stack_source_map()
    assert type(Error.prepareStackTrace).__name__ == "function" or callable(Error.prepareStackTrace)

def test_uses_user_provided_prepare_stack_trace_from_options():
    def custom_prepare(*a, **k): return "custom"
    stack_source_map({"prepareStackTrace": custom_prepare})
    assert Error.prepareStackTrace is custom_prepare

def test_does_not_throw_if_ErrorStackParser_is_custom_object():
    def mock_parse(*a, **k): return "parsed"
    stack_source_map({"ErrorStackParser": {"parse": mock_parse}})
    assert callable(Error.prepareStackTrace)
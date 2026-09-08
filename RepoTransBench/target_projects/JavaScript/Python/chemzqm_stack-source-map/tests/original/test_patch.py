import pytest
from src.stack_source_map import stack_source_map

def test_should_handle_repeated_calls():
    # Should not throw if called multiple times
    stack_source_map()
    stack_source_map()
    stack_source_map({})

def test_should_not_throw_if_called_with_bogus_options():
    stack_source_map({"foo": 123, "bar": False})

def test_should_allow_override_of_options():
    prepare_stack = lambda x: "done"
    stack_source_map({"prepareStackTrace": prepare_stack})
    stack_source_map()
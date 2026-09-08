import pytest

# Import stubs from original test modules
from tests.original.test_app import App, ObjectGraph

def test_on_terminate_multiple_calls():
    app = App()
    app.on_terminate()
    app.on_terminate()  # Call it multiple times

def test_build_object_graph_and_inject_multiple_times():
    app = App()
    app.build_object_graph_and_inject()
    app.build_object_graph_and_inject()  # Call multiple times
    assert app.get_application_graph() is not None

def test_inject_with_string_object():
    app = App()
    app.build_object_graph_and_inject()
    some_obj = "HelloPublic"
    app.inject(some_obj)
    assert app.get_application_graph() is not None

def test_create_scoped_graph_with_longer_name():
    app = App()
    app.build_object_graph_and_inject()
    scoped = app.create_scoped_graph("publicModExtra")
    assert scoped is not None
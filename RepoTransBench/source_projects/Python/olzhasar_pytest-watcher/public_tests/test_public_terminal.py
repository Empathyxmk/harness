from pytest_watcher.terminal import Terminal

def test_terminal_type_and_methods():
    term = Terminal()
    # Should at least have __str__ attribute (different from __class__)
    assert hasattr(term, "__str__")

def test_terminal_instance_not_false():
    term = Terminal()
    # confirm instance is truthy (not False)
    assert bool(term) is True
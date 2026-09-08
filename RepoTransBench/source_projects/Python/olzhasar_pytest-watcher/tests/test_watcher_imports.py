import pytest
import pytest_watcher.watcher

def test_imports_and_main_loop_present():
    assert hasattr(pytest_watcher.watcher, "main_loop")
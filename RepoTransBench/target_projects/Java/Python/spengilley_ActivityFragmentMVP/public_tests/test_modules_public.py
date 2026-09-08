import pytest

from tests.original.test_app import App
from tests.original.test_modules import Modules, AppModule

def test_list_non_null_different_app_instance():
    # Use a different App() instance (structurally equal, still different from original test instance)
    test_app = App()
    modules = Modules.list(test_app)
    assert modules is not None
    assert len(modules) > 0
    assert type(modules[0]) is AppModule
import pytest

from tests.original.test_app import App
from tests.original.test_modules import AppModule

def test_provide_application_different_app_instance():
    # Use a different App() instance than the original test
    another_app = App()
    module = AppModule(another_app)
    returned = module.provide_application()
    assert returned is another_app  # Checks reference equality
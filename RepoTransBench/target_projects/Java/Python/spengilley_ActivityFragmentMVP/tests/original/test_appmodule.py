import pytest

from tests.original.test_app import App
from tests.original.test_modules import AppModule

def test_provide_application_returns_app():
    app = App()
    module = AppModule(app)
    returned = module.provide_application()
    assert returned == app